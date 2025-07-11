<script lang="ts">
	import AspectRatio from "$lib/components/ui/aspect-ratio/aspect-ratio.svelte";
	import UploadImage from "$lib/components/ui/uploadImage/uploadImage.svelte";
	import Label from "../ui/label/label.svelte";
</script>

<div class="flex flex-col w-sm gap-2">
    <div class="flex flex-col gap-1">
        <Label for="image-preview">Image Preview</Label>
        <AspectRatio ratio={1} class="border-2 rounded-lg bg-muted" id="image-preview">
            <img src="/images/giraffe-compressed.jpg" alt="..." class="w-full h-full rounded-lg object-cover" />
        </AspectRatio>
    </div>
    <UploadImage/>
</div>