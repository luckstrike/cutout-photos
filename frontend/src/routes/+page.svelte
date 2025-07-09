<script lang="ts">
    import { Button } from "$lib/components/ui/button/index.js";
    import { Slider } from "$lib/components/ui/slider/index.js";
    
    let value = $state(50);
</script>
 
<Button>Click me</Button>
<Slider type="single" bind:value max={100} step={1} class="max-w-[70%]" />