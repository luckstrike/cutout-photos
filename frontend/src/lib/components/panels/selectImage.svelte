<script lang="ts">
	import AspectRatio from '$lib/components/ui/aspect-ratio/aspect-ratio.svelte';
	import Input from "$lib/components/ui/input/input.svelte";
	import Label from '$lib/components/ui/label/label.svelte';

    interface Props {
        selectedFile?: File | null;
        displayImageUrl?: string | null;
        isLoading?: boolean;
    }

    let { 
        selectedFile = $bindable(null),
        displayImageUrl = null,
        isLoading = false
     } : Props = $props();

    let files : FileList | undefined = $state(undefined);

    $effect(() => {
        if (files && files.length > 0) {
            selectedFile = files[0];
        }
    });
</script>

<div class="w-sm flex flex-col gap-2">
	<div class="flex flex-col gap-1">
		<Label for="image-preview">Image Preview</Label>
		<AspectRatio ratio={1} class="bg-muted rounded-lg border-2" id="image-preview">
            {#if displayImageUrl}
                <img
                    src={displayImageUrl}
                    alt="..."
                    class="h-full w-full rounded-lg object-cover text-center"
                />
                {#if isLoading}
                    <div class="absolute inset-0 flex items-center justify-center">
                        <div class="text-sm font-medium">Processing...</div>
                    </div>
                {/if}
            {/if}
		</AspectRatio>
	</div>
    <div class="flex flex-col w-full gap-1">
        <Label for="picture">Select an Image to Upload</Label>
        <div class="flex flex-1 gap-1">
            <Input 
                accept="image/*"
                bind:files
                class="flex"
                id="picture"
                type="file" 
            />
        </div>
    </div>
</div>
