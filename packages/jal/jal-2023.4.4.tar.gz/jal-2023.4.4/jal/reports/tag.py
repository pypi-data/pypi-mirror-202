from PySide6.QtCore import Slot, QObject
from jal.db.ledger import Ledger
from jal.reports.reports import Reports
from jal.db.operations import LedgerTransaction
from jal.db.operations_model import OperationsModel
from jal.ui.reports.ui_tag_report import Ui_TagReportWidget
from jal.widgets.mdi import MdiWidget

JAL_REPORT_CLASS = "TagReport"


# ----------------------------------------------------------------------------------------------------------------------
class TagOperationsModel(OperationsModel):
    def __init__(self, parent_view):
        self._tag_id = 0
        super().__init__(parent_view)

    def setTag(self, tag):
        self._tag_id = tag
        self.prepareData()

    def prepareData(self):
        self._data = []
        self._data = Ledger.get_operations_by_tag(self._begin, self._end, self._tag_id)
        self.modelReset.emit()


# ----------------------------------------------------------------------------------------------------------------------
class TagReport(QObject):
    def __init__(self):
        super().__init__()
        self.group = self.tr("Operations")
        self.name = self.tr("by Tag")
        self.window_class = "TagReportWindow"


# ----------------------------------------------------------------------------------------------------------------------
class TagReportWindow(MdiWidget, Ui_TagReportWidget):
    def __init__(self, parent: Reports, settings: dict = None):
        MdiWidget.__init__(self, parent.mdi_area())
        self.setupUi(self)
        self._parent = parent

        self.tag_model = TagOperationsModel(self.ReportTableView)
        self.ReportTableView.setModel(self.tag_model)
        self.tag_model.configureView()

        self.connect_signals_and_slots()

        if settings is not None:
            self.ReportRange.setRange(settings['begin_ts'], settings['end_ts'])
            self.ReportTagEdit.selected_id = settings['tag_id']
            self.onTagChange()

    def connect_signals_and_slots(self):
        self.ReportRange.changed.connect(self.ReportTableView.model().setDateRange)
        self.ReportTagEdit.changed.connect(self.onTagChange)
        self.ReportTableView.selectionModel().selectionChanged.connect(self.onOperationSelect)

    @Slot()
    def onTagChange(self):
        self.ReportTableView.model().setTag(self.ReportTagEdit.selected_id)

    @Slot()
    def onOperationSelect(self, selected, _deselected):
        idx = selected.indexes()
        if idx:
            selected_row = idx[0].row()
            operation_type, operation_id = self.ReportTableView.model().get_operation(selected_row)
            self.OperationDetails.show_operation(operation_type, operation_id)
        else:
            self.OperationDetails.show_operation(LedgerTransaction.NA, 0)
