<script lang="ts">
    let hexCode : string = $state("#000000");
    let sliderColor : string = $state("#0000FF");
</script>

<div class="flex">
    <div class=""></div>
    <canvas class="color-gradient w-50 h-50" style="--sliderColor: {sliderColor}"></canvas>
</div>

<style>
    .color-gradient {
        background-image: 
            linear-gradient(to bottom, transparent, #000000),
            linear-gradient(to right, #ffffff, var(--sliderColor));
    }
</style>