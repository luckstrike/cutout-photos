<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
    import Input from "$lib/components/ui/input/input.svelte";
    import Upload from "@lucide/svelte/icons/upload";
    import FileCheck from "@lucide/svelte/icons/file-check";
	import Label from "../label/label.svelte";

    let files = $state(undefined);
</script>

<div class="flex w-full">
    {#if files}
        <div class="flex flex-col gap-1">
            <Label for="picture">Select an Image to Upload</Label>
            <div class="flex gap-1">
                <Input 
                    accept="image/*"
                    bind:files
                    class="flex"
                    id="picture"
                    type="file" 
                />
                <Button variant="outline" class="flex">
                    <Upload />
                </Button>
            </div>
        </div>
    {:else}
        <div class="flex flex-col gap-1">
            <Label for="picture">Select an Image to Upload</Label>
            <div class="flex gap-1">
                <Input 
                    accept="image/*"
                    bind:files
                    class="flex text-gray-500"
                    id="picture"
                    type="file" 
                />
                <Button variant="outline" class="flex" disabled>
                    <Upload />
                </Button>
            </div>
        </div>
    {/if}
</div>