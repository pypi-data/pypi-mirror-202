<template>
	<div class="CoreNumberInput" ref="rootEl">
		<div class="main">
			<div class="inputContainer">
				<label>{{ fields.label }}</label>
				<input
					type="number"
					v-on:input="($event) => handleInput(($event.target as HTMLInputElement).value, 'ss-change-number')"
					:value="formValue"
					:placeholder="fields.placeholder"
				/>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../../streamsyncTypes";

const description =
	"A user input component that allows users to enter numeric values.";

export default {
	streamsync: {
		name: "Number Input",
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
				type: FieldType.Number,
			},
			placeholder: {
				name: "Placeholder",
				type: FieldType.Text,
			},
		},
		events: {
			"ss-change-number": {
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

.CoreNumberInput {
	width: fit-content;
}

label {
	display: block;
	margin-bottom: 8px;
	color: var(--primaryTextColor);
}

input {
	max-width: 70ch;
	min-width: 30ch;
	width: 100%;
	margin: 0;
	border: 1px solid var(--separatorColor);
}
</style>
