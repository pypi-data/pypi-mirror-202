<template>
	<div class="CoreDateInput" ref="rootEl">
		<div class="main">
			<div class="inputContainer">
				<label>{{ fields.label }}</label>
				<input
					type="date"
					:value="formValue"
					v-on:input="($event) => handleInput(($event.target as HTMLInputElement).value, 'ss-change')"
				/>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../../streamsyncTypes";

const description =
	"A user input component that allows users to select a date using a date picker interface.";

export default {
	streamsync: {
		name: "Date Input",
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
import { inject, Ref, ref } from "vue";
import injectionKeys from "../../injectionKeys";
import { useFormValueBroker } from "../../renderer/useFormValueBroker";

const fields = inject(injectionKeys.evaluatedFields);
const rootEl: Ref<HTMLElement> = ref(null);
const ss = inject(injectionKeys.core);
const componentId = inject(injectionKeys.componentId);

const { formValue, handleInput } = useFormValueBroker(ss, componentId, rootEl);
</script>

<style scoped>
@import "../../renderer/sharedStyles.css";

.CoreDateInput {
	width: fit-content;
}

label {
	display: block;
	margin-bottom: 8px;
}

input {
	max-width: 20ch;
	width: 100%;
	margin: 0;
	border: 1px solid var(--separatorColor);
}
</style>
