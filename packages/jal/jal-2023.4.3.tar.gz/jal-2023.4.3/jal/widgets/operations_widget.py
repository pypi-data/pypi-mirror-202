from functools import partial

from PySide6.QtCore import Qt, Slot, Signal, QDateTime, QSortFilterProxyModel
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMessageBox
from jal.ui.ui_operations_widget import Ui_OperationsWidget
from jal.widgets.mdi import MdiWidget
from jal.db.helpers import load_icon
from jal.db.account import JalAccount
from jal.db.asset import JalAsset
from jal.db.balances_model import BalancesModel
from jal.db.operations_model import OperationsModel
from jal.db.operations import LedgerTransaction


# ----------------------------------------------------------------------------------------------------------------------
class OperationsWidget(MdiWidget, Ui_OperationsWidget):
    dbUpdated = Signal()

    def __init__(self, parent=None):
        MdiWidget.__init__(self, parent)
        self.setupUi(self)

        self.current_index = None  # this is used in onOperationContextMenu() to track item for menu

        # Set icons
        self.NewOperationBtn.setIcon(load_icon("new.png"))
        self.CopyOperationBtn.setIcon(load_icon("copy.png"))
        self.DeleteOperationBtn.setIcon(load_icon("delete.png"))

        # Operations view context menu
        self.contextMenu = QMenu(self.OperationsTableView)
        self.actionReconcile = QAction(load_icon("reconcile.png"), self.tr("Reconcile"), self)
        self.actionCopy = QAction(load_icon("copy.png"), self.tr("Copy"), self)
        self.actionDelete = QAction(load_icon("delete.png"), self.tr("Delete"), self)
        self.contextMenu.addAction(self.actionReconcile)
        self.contextMenu.addSeparator()
        self.contextMenu.addAction(self.actionCopy)
        self.contextMenu.addAction(self.actionDelete)

        # Customize UI configuration
        self.balances_model = BalancesModel(self.BalancesTableView)
        self.BalancesTableView.setModel(self.balances_model)
        self.balances_model.configureView()

        self.operations_model = OperationsModel(self.OperationsTableView)
        self.operations_filtered_model = QSortFilterProxyModel(self.OperationsTableView)
        self.operations_filtered_model.setSourceModel(self.operations_model)
        self.operations_filtered_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.OperationsTableView.setModel(self.operations_filtered_model)
        self.operations_model.configureView()
        self.OperationsTableView.setContextMenuPolicy(Qt.CustomContextMenu)

        self.connect_signals_and_slots()

        self.NewOperationMenu = QMenu()
        self.OperationsTabs.dbUpdated.connect(self.dbUpdated)
        self.OperationsTabs.dbUpdated.connect(self.operations_model.refresh)
        for key, name in self.OperationsTabs.get_operations_list().items():
            self.NewOperationMenu.addAction(name, partial(self.createOperation, key))
        self.NewOperationBtn.setMenu(self.NewOperationMenu)

        # Setup balance and holdings parameters
        current_time = QDateTime.currentDateTime()
        current_time.setTimeSpec(Qt.UTC)  # We use UTC everywhere so need to force TZ info
        self.BalanceDate.setDateTime(current_time)
        self.BalancesCurrencyCombo.setIndex(JalAsset.get_base_currency())

        self.OperationsTableView.selectRow(0)
        self.DateRange.setCurrentIndex(0)

    def connect_signals_and_slots(self):
        self.actionReconcile.triggered.connect(self.reconcileAtCurrentOperation)
        self.BalanceDate.dateChanged.connect(self.BalancesTableView.model().setDate)
        self.BalancesCurrencyCombo.changed.connect(self.BalancesTableView.model().setCurrency)
        self.BalancesTableView.doubleClicked.connect(self.OnBalanceDoubleClick)
        self.ShowInactiveCheckBox.stateChanged.connect(self.BalancesTableView.model().toggleActive)
        self.DateRange.changed.connect(self.operations_model.setDateRange)
        self.ChooseAccountBtn.changed.connect(self.operations_model.setAccount)
        self.SearchString.editingFinished.connect(self.updateOperationsFilter)
        self.OperationsTableView.selectionModel().selectionChanged.connect(self.OnOperationChange)
        self.OperationsTableView.customContextMenuRequested.connect(self.onOperationContextMenu)
        self.DeleteOperationBtn.clicked.connect(self.deleteOperation)
        self.actionDelete.triggered.connect(self.deleteOperation)
        self.CopyOperationBtn.clicked.connect(self.OperationsTabs.copy_operation)
        self.actionCopy.triggered.connect(self.OperationsTabs.copy_operation)

    @Slot()
    def deleteOperation(self):
        if QMessageBox().warning(None, self.tr("Confirmation"),
                                 self.tr("Are you sure to delete selected transacion(s)?"),
                                 QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
            return
        rows = []
        for index in self.OperationsTableView.selectionModel().selectedRows():
            rows.append(index.row())
        self.operations_model.deleteRows(rows)
        self.dbUpdated.emit()

    @Slot()
    def createOperation(self, operation_type):
        self.OperationsTabs.new_operation(operation_type, self.operations_model.getAccount())

    @Slot()
    def updateOperationsFilter(self):
        self.OperationsTableView.model().setFilterFixedString(self.SearchString.text())
        self.OperationsTableView.model().setFilterKeyColumn(-1)

    @Slot()
    def OnBalanceDoubleClick(self, index):
        self.ChooseAccountBtn.account_id = index.model().getAccountId(index.row())

    @Slot()
    def OnOperationChange(self, selected, _deselected):
        op_type = LedgerTransaction.NA
        op_id = 0
        if len(self.OperationsTableView.selectionModel().selectedRows()) == 1:
            idx = selected.indexes()
            if idx:
                selected_row = self.operations_filtered_model.mapToSource(idx[0]).row()
                op_type, op_id = self.operations_model.get_operation(selected_row)
        self.OperationsTabs.show_operation(op_type, op_id)

    @Slot()
    def onOperationContextMenu(self, pos):
        self.current_index = self.OperationsTableView.indexAt(pos)
        if len(self.OperationsTableView.selectionModel().selectedRows()) != 1:
            self.actionReconcile.setEnabled(False)
            self.actionCopy.setEnabled(False)
        else:
            self.actionReconcile.setEnabled(True)
            self.actionCopy.setEnabled(True)
        self.contextMenu.popup(self.OperationsTableView.viewport().mapToGlobal(pos))

    @Slot()
    def reconcileAtCurrentOperation(self):
        idx = self.operations_model.index(self.current_index.row(), 0)  # we need only row to address fields by name
        timestamp = self.operations_model.data(idx, Qt.UserRole, field="timestamp")
        account_id = self.operations_model.data(idx, Qt.UserRole, field="account_id")
        JalAccount(account_id).reconcile(timestamp)
        self.operations_model.refresh()

    def refresh(self):
        self.balances_model.update()
