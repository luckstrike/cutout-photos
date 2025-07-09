<script lang="ts">
    import { Slider } from "$lib/components/ui/slider/index.js";
    
    let outlineThickness = $state(50);
    let detailValue = $state(25);
</script>

<div class="flex-col w-100 space-y-4 border-1 rounded-2xl p-4">
    <div class="space-y-2">
        <p>Outline Thickness</p>
        <Slider type="single" bind:value={outlineThickness} max={100} step={1} class="max-w" />
    </div>
    
    <div class="space-y-2">
        <p>Detail Value</p>
        <Slider type="single" bind:value={detailValue} max={50} step={1} class="max-w" />
    </div>
    <div class="space-y-2">
        <p>Outline Color</p>
    </div>
</div>