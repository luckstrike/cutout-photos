<script lang="ts">
    import CutoutOptions from "$lib/components/panels/cutoutOptions.svelte";
    import Navbar from "$lib/components/panels/navbar.svelte";
</script>

<div class="flex-col w-screen h-screen p-4 space-y-4">
    <Navbar />
    <h1 class="text-3xl font-semibold">Create a Cutout</h1>
    <div class="flex justify-between">
        <div>Insert a preview of the image here</div>
        <CutoutOptions/>        
    </div>
</div>