import { computed, Ref, ref, watch } from "vue";
import { Component, Core } from "../streamsyncTypes";

/**
 *
 * Encapsulates repeatable form value logic, including binding.
 *
 * @param ss
 * @param componentId
 * @returns
 */
export function useFormValueBroker(
	ss: Core,
	componentId: Component["id"],
	emitterEl: Ref<HTMLElement>
) {
	const formValue = computed({
		get() {
			return ss.getFormValue(componentId);
		},
		set(newValue) {
			ss.setFormValue(componentId, newValue);
		},
	});
	const isBusy = ref(false);
	const queuedEvent: Ref<{ eventValue: any; emitEventType: string }> =
		ref(null);

	/**
	 * Takes a value and emits a CustomEvent of the given type.
	 * Deals with debouncing.
	 *
	 * @param newValue
	 * @param emitEventType
	 * @returns
	 */
	function handleInput(eventValue: any, emitEventType: string) {
		if (isBusy.value) {
			// Queued event is overwritten for debouncing purposes

			queuedEvent.value = {
				eventValue,
				emitEventType,
			};
			return;
		}

		formValue.value = eventValue;
		isBusy.value = true;
		const callback = () => {
			isBusy.value = false;
			if (!queuedEvent.value) return;
			handleInput(
				queuedEvent.value.eventValue,
				queuedEvent.value.emitEventType
			);
			queuedEvent.value = null;
		};

		const event = new CustomEvent(emitEventType, {
			detail: {
				payload: eventValue,
				callback,
			},
		});
		emitterEl.value.dispatchEvent(event);
	}

	watch(
		() => ss.getBindingValue(componentId),
		(value) => {
			if (isBusy.value) return;
			if (typeof value == "undefined") return;
			formValue.value = value;
		},
		{ immediate: true }
	);

	watch(
		formValue,
		(newValue) => {
			if (typeof newValue === "undefined") {
				formValue.value = "";
			}
		},
		{ immediate: true }
	);

	return {
		formValue,
		handleInput,
	};
}
