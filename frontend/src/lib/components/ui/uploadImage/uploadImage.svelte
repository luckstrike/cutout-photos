<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
    import Input from "$lib/components/ui/input/input.svelte";
    import Upload from "@lucide/svelte/icons/upload";
	import Label from "../label/label.svelte";

    let { onFileSelect } = $props();
    let files : FileList | undefined = $state(undefined);

    $effect(() => {
        if (files && files.length > 0) {
            onFileSelect(files[0])       
        }
    });

</script>

<div class="flex w-full">
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