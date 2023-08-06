<template>
	<div class="CoreVideoPlayer">
		<video
			:src="fields.src"
			:controls="fields.controls === 'yes'"
			:autoplay="fields.autoplay === 'yes'"
			:loop="fields.loop === 'yes'"
			:muted="fields.muted === 'yes'"
		></video>
	</div>
</template>

<script lang="ts">
import { FieldCategory, FieldType } from "../streamsyncTypes";

const description =
	"A video player component that can play various video formats.";

export default {
	streamsync: {
		name: "Video Player",
		description,
		category: "Content",
		fields: {
			src: {
				name: "Source",
				desc: "The URL, which might be a data URL, of the video file.",
				default: "",
				type: FieldType.Text,
			},
			controls: {
				name: "Controls",
				desc: "Display video player controls.",
				default: "yes",
				type: FieldType.Text,
				options: {
					yes: "Yes",
					no: "No",
				},
			},
			autoplay: {
				name: "Autoplay",
				desc: "Autoplay the video when the component is loaded.",
				default: "no",
				type: FieldType.Text,
				options: {
					yes: "Yes",
					no: "No",
				},
			},
			loop: {
				name: "Loop",
				desc: "Loop the video when it reaches the end.",
				default: "no",
				type: FieldType.Text,
				options: {
					yes: "Yes",
					no: "No",
				},
			},
			muted: {
				name: "Muted",
				desc: "Mute the video by default.",
				default: "no",
				type: FieldType.Text,
				options: {
					yes: "Yes",
					no: "No",
				},
			},
		},
	},
};
</script>

<script setup lang="ts">
import { inject } from "vue";
import injectionKeys from "../injectionKeys";

const fields = inject(injectionKeys.evaluatedFields);
</script>

<style scoped>
.CoreVideoPlayer {
	width: 100%;
}

video {
	width: 100%;
}
</style>
