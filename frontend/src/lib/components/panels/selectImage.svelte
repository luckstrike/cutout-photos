<script lang="ts">
	import AspectRatio from '$lib/components/ui/aspect-ratio/aspect-ratio.svelte';
	import UploadImage from '$lib/components/ui/uploadImage/uploadImage.svelte';
	import Label from '../ui/label/label.svelte';

    let selectedFile : File | null = $state(null);
    let imageURL : string | null = $derived(selectedFile ? URL.createObjectURL(selectedFile) : null);

    interface Props {
        handleFileSelect?: (file: File | null) => void;
    }

    let { handleFileSelect = () => {} } : Props = $props();

    function onFileSelect(file: File) {
        if (!file) {
            return;
        }

        selectedFile = file;
        handleFileSelect(selectedFile);
    }

    // Cleanup Function
    $effect(() => {
        return () => {
            if (imageURL) {
                URL.revokeObjectURL(imageURL);
            }
        };
    });
</script>

<div class="w-sm flex flex-col gap-2">
	<div class="flex flex-col gap-1">
		<Label for="image-preview">Image Preview</Label>
		<AspectRatio ratio={1} class="bg-muted rounded-lg border-2" id="image-preview">
            {#if selectedFile}
                <img
                    src={imageURL}
                    alt="..."
                    class="h-full w-full rounded-lg object-cover text-center"
                />
            {/if}
		</AspectRatio>
	</div>
	<UploadImage {onFileSelect} />
</div>
