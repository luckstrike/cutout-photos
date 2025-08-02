<script lang="ts">
    import { Slider } from "$lib/components/ui/slider/index.js";
	import Button from "$lib/components/ui/button/button.svelte";
	import Label from "$lib/components/ui/label/label.svelte";
	import ColorPicker from "../ui/colorPicker/colorPicker.svelte";
    
    let outlineThickness = $state(50);
    let detailValue = $state(25);
    let outlineColor = $state("");

    interface Props {
        handleOutlineThicknessChange?: (thickness: number) => void;
        handleDetailValueChange?: (detail: number) => void;
        handleOutlineColorChange?: (hexColor: string) => void;
    }

    let { 
        handleOutlineThicknessChange = () => {},
        handleDetailValueChange = () => {},
        handleOutlineColorChange = () => {}
    } = $props();

    function onOutlineColorChange(hexColor: string) {
        outlineColor = hexColor;
    }

    $effect(() => {
        handleOutlineThicknessChange(outlineThickness);
        handleDetailValueChange(detailValue);
        handleOutlineColorChange(outlineColor);
    })

</script>

<div class="flex flex-col min-w-xs gap-4 border-1 rounded-2xl p-4">
    <div class="flex flex-col text-xl font-bold gap-1">
        <div>Cutout Options</div>
        <hr class="border-1" />
    </div>
    <div class="flex flex-col gap-2">
        <Label for="outline-value">Outline Thickness</Label>
        <Slider type="single" bind:value={outlineThickness} max={100} step={1} class="max-w" id="outline-value" />
    </div>
    
    <div class="flex flex-col gap-2">
        <Label for="detail-value">Detail Value</Label>
        <Slider type="single" bind:value={detailValue} max={50} step={1} class="max-w" id="detail-value" />
    </div>
    <div class="flex flex-col gap-2">
        <Label for="outline-color">Outline Color</Label>
        <ColorPicker onHexColorChange={onOutlineColorChange}/>
    </div>
    <div>
        <Button variant="outline">Create Cutout</Button>
    </div>
</div>