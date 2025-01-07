    def update_vertical_label(graph_selected, trace_selected, slider_data):
        """
        Updates the vertical offset label name dynamically when a graph and trace are selected.
        """

        # ✅ Get the correct trace unit from the global dictionary
        trace_units = gd.global_graph_dictionary[graph_selected]["traces_metadata_from_name"][trace_selected][1]

        # ✅ Ensure stored data exists
        if not slider_data or "default_labels" not in slider_data:
            vertical_label = f"{trace_units} Offset: 0"
        else:
            current_value = slider_data["default_labels"].get("vertical", "0").split(":")[-1].strip()
            vertical_label = f"{trace_units} Offset: {current_value}"

        return vertical_label