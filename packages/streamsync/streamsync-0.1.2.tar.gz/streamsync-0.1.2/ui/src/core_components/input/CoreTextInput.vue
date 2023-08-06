<template>
	<div class="CoreTextInput" ref="rootEl">
		<label>{{ fields.label }}</label>
		<input
			type="text"
			:value="formValue"
			v-on:input="($event) => handleInput(($event.target as HTMLInputElement).value, 'ss-change')"
			:placeholder="fields.placeholder"
		/>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../../streamsyncTypes";

const description =
	"A user input component that allows users to enter single-line text values.";

export default {
	streamsync: {
		name: "Text Input",
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

.CoreTextInput {
	max-width: 70ch;
	width: 100%;
}

label {
	display: block;
	margin-bottom: 8px;
	color: var(--primaryTextColor);
}

input {
	margin: 0;
	border: 1px solid var(--separatorColor);
}
</style>
