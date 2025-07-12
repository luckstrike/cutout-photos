<script lang="ts">
	import AspectRatio from '$lib/components/ui/aspect-ratio/aspect-ratio.svelte';
	import UploadImage from '$lib/components/ui/uploadImage/uploadImage.svelte';
	import Label from '../ui/label/label.svelte';

    let maxFileSize : number = 5000000; // 5MB

    let selectedFile : File | null = $state(null);
    let imageURL : string | null = $derived(selectedFile ? URL.createObjectURL(selectedFile) : null);

	function handleFileSelect(file: File) {
        if (file && file.type.startsWith('image/') && file.size < maxFileSize) {
            selectedFile = file;
        } else {
            // TODO: Change this to a Toast
            alert('Please select a valid image under 5MB')
        }
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
	<UploadImage onFileSelect={handleFileSelect} />
</div>
