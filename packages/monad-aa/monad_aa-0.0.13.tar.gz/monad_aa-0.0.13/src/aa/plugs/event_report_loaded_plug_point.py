class ReportLoadedPlugPoint:
    def __init__(self):
        pass

    def emit_event(self, event_name, event_payload):
        pass

    def register_event_emitter(self, event_name, event_payload_model):
        """
        This I think should go to framework as boiler plate code

        :param event_name: name of the event
        :param event_payload_model: name of the model class.
            TODO think about how to implement this.
        :return:
        """
        pass

    def publish_event(self, event_name, event_payload_kwargs):
        """
        this method produces an event indicating report has been loaded.

        publisher produces event.

        payload: report_id, account_number, date

        :param event_name:
        :param event_payload_kwargs:
        :return:
        """
        # TODO get this from karyastala
        pass
