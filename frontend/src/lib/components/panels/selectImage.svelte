<script lang="ts">
	import { panzoom } from '$lib/actions/panzoom';
	import AspectRatio from '$lib/components/ui/aspect-ratio/aspect-ratio.svelte';
	import Input from "$lib/components/ui/input/input.svelte";
	import Label from '$lib/components/ui/label/label.svelte';
	import { RefreshCw } from '@lucide/svelte';
import { Button } from '$lib/components/ui/button';

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
    let ctrl: any;

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
                <div class="relative h-full w-full">
                    <img
                        use:panzoom={{ onInit: (c: any) => (ctrl = c)}}
                        src={displayImageUrl}
                        alt="Selected image preview"
                        onload={() => (ctrl as any)?.reset?.({} as any)}
                        draggable="false"
                        class="h-full w-full rounded-lg object-contain text-center touch-none"
                        style="image-rendering: auto;"
                    />

                    <Button
                        variant="outline"
                        size="icon"
                        class="absolute top-2 right-2 z-40 bg-opacity-70 backdrop-blur-sm"
                        aria-label="Reset view"
                        onclick={(e: MouseEvent) => { e.stopPropagation(); return (ctrl ? (ctrl as any).reset?.({ animate: true } as any) : null); }}
                        onpointerdown={(e: PointerEvent) => e.stopPropagation()}
                        style="pointer-events: auto;"
                        tabindex={0}
                    >
                        <RefreshCw class="h-4 w-4" aria-hidden="true" />
                        <span class="sr-only">Reset view</span>
                    </Button>

                    {#if isLoading}
                        <div class="absolute inset-0 flex items-center justify-center">
                            <div class="text-sm font-medium">Processing...</div>
                        </div>
                    {/if}
                </div>
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
