<script lang="ts">
	import AspectRatio from "../ui/aspect-ratio/aspect-ratio.svelte";
</script>

<div class="flex flex-col w-sm gap-2">
    <AspectRatio ratio={1} class="border-2 rounded-lg bg-muted">
        <img src="/images/giraffe-compressed.jpg" alt="..." class="w-full h-full rounded-lg object-cover" />
    </AspectRatio>
    <div>
        Upload an image
    </div>
</div>