<template>
	<div class="CoreFileInput" ref="rootEl">
		<div class="main">
			<div class="inputContainer">
				<label>{{ fields.label }}</label>
				<input
					type="file"
					ref="fileEl"
					v-on:change="fileChange($event as InputEvent)"
					:multiple="allowMultipleFilesFlag"
				/>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../../streamsyncTypes";

const MAX_FILE_SIZE = 200 * 1024 * 1024;

const description = "A user input component that allows users to upload files.";

export default {
	streamsync: {
		name: "File Input",
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
				desc: "Assigns a key to be used when processing a Form submission.",
			},
			allowMultipleFiles: {
				name: "Allow multiple files",
				init: "no",
				type: FieldType.Text,
				options: {
					yes: "Yes",
					no: "No",
				},
			},
		},
		events: {
			"ss-file-change": {
				desc: "Capture changes to this control.",
				bindable: true,
			},
		},
	},
};
</script>

<script setup lang="ts">
import { computed, inject, Ref, ref, watch } from "vue";
import injectionKeys from "../../injectionKeys";
import { useFormValueBroker } from "../../renderer/useFormValueBroker";

const fields = inject(injectionKeys.evaluatedFields);
const rootEl: Ref<HTMLInputElement> = ref(null);
const fileEl: Ref<HTMLInputElement> = ref(null);
const ss = inject(injectionKeys.core);
const componentId = inject(injectionKeys.componentId);

const { formValue, handleInput } = useFormValueBroker(ss, componentId, rootEl);

const allowMultipleFilesFlag = computed(() => {
	return fields.value.allowMultipleFiles == "yes" ? true : undefined;
});

const encodeFile = async (file: File) => {
	var reader = new FileReader();
	reader.readAsDataURL(file);

	return new Promise((resolve, reject) => {
		reader.onload = () => resolve(reader.result);
		reader.onerror = () => reject(reader.error);
	});
};

const fileChange = async (ev: InputEvent) => {
	const el = ev.target as HTMLInputElement;
	if (!el.files || el.files.length == 0) return;

	const getValue = async () => {
		const encodedFiles = Promise.all(
			Array.from(el.files).map(async (f) => {
				if (f.size > MAX_FILE_SIZE) {
					throw `File ${f.name} is too big. File size limit is 200mb.`;
				}
				const fileItem = {
					name: f.name,
					type: f.type,
					data: await encodeFile(f),
				};
				return fileItem;
			})
		);
		return encodedFiles;
	};

	formValue.value = getValue();

	handleInput(getValue(), "ss-file-change");
};

watch(formValue, (newValue: string) => {
	if (typeof newValue === "undefined" && fileEl.value) {
		fileEl.value.value = "";
	}
});
</script>

<style scoped>
@import "../../renderer/sharedStyles.css";

.CoreFileInput {
	width: 100%;
}

label {
	display: block;
	margin-bottom: 8px;
}

input {
	max-width: 70ch;
	width: 100%;
	margin: 0;
	border: 1px solid var(--separatorColor);
}
</style>
