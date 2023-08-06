<template>
	<div class="CoreTextareaInput" ref="rootEl">
		<label>{{ fields.label }}</label>
		<textarea
			:value="formValue"
			v-on:input="($event) => handleInput(($event.target as HTMLTextAreaElement).value, 'ss-change')"
			:placeholder="fields.placeholder"
			:rows="fields.rows"
		></textarea>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../../streamsyncTypes";

const description =
	"A user input component that allows users to enter multi-line text values.";

export default {
	streamsync: {
		name: "Textarea Input",
		description,
		category: "Input",
		fields: {
			label: {
				name: "Label",
				init: "Input Label",
				type: FieldType.Text,
			},
			key: {
				name: "Key",
				type: FieldType.Text,
				desc: "Used to identify the value during form submission.",
			},
			initialValue: {
				name: "Initial value",
				type: FieldType.Text,
				default: "",
			},
			placeholder: {
				name: "Placeholder",
				type: FieldType.Text,
				control: "textarea",
			},
			rows: {
				name: "Rows",
				type: FieldType.Number,
				init: "5",
				default: "5",
			},
		},
		events: {
			"ss-change": {
				desc: "Capture changes to this control.",
				bindable: true,
			},
		},
	},
};
</script>

<script setup lang="ts">
import { inject, ref } from "vue";
import injectionKeys from "../../injectionKeys";
import { useFormValueBroker } from "../../renderer/useFormValueBroker";

const fields = inject(injectionKeys.evaluatedFields);
const rootEl = ref(null);
const ss = inject(injectionKeys.core);
const componentId = inject(injectionKeys.componentId);

const { formValue, handleInput } = useFormValueBroker(ss, componentId, rootEl);
</script>

<style scoped>
@import "../../renderer/sharedStyles.css";

.CoreTextareaInput {
	max-width: 70ch;
	width: 100%;
}

label {
	display: block;
	margin-bottom: 8px;
	color: var(--primaryTextColor);
}

textarea {
	width: 100%;
	margin: 0;
	border: 1px solid var(--separatorColor);
	resize: vertical;
}
</style>
