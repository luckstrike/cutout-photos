<script lang="ts">
    let canvas: HTMLCanvasElement;
    let hexColor = $state("#0000ff");
    let hue = $state(240);
    let dragging = $state(false);

    const SIZE = 200;

    function getPixelColor(event: MouseEvent) {
        const ctx = canvas.getContext('2d')!;
        const [r, g, b] = ctx.getImageData(event.offsetX, event.offsetY, 1, 1).data;
        hexColor = `#${[r, g, b].map(c => c.toString(16).padStart(2, '0')).join('')}`;
    }

    function drawGradient() {
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d')!;
        ctx.clearRect(0, 0, SIZE, SIZE);

        // White to hue
        const hGrad = ctx.createLinearGradient(0, 0, SIZE, 0);
        hGrad.addColorStop(0, '#fff');
        hGrad.addColorStop(1, `hsl(${hue}, 100%, 50%)`);
        ctx.fillStyle = hGrad;
        ctx.fillRect(0, 0, SIZE, SIZE);

        // Transparent to black
        const vGrad = ctx.createLinearGradient(0, 0, 0, SIZE);
        vGrad.addColorStop(0, 'transparent');
        vGrad.addColorStop(1, '#000');
        ctx.fillStyle = vGrad;
        ctx.fillRect(0, 0, SIZE, SIZE);
    }

    function updateHue(event: MouseEvent) {
        const rect = event.currentTarget.getBoundingClientRect();
        const y = Math.max(0, Math.min(SIZE, event.clientY - rect.top));
        hue = Math.round((y / SIZE) * 360);
    }

    function startDrag(event: MouseEvent) {
        dragging = true;
        updateHue(event);
    }

    function handleGlobalMove(event: MouseEvent) {
        if (!dragging) return;
        const slider = document.querySelector('[data-hue-slider]') as HTMLElement;
        if (slider) {
            const rect = slider.getBoundingClientRect();
            const y = Math.max(0, Math.min(SIZE, event.clientY - rect.top));
            hue = Math.round((y / SIZE) * 360);
        }
    }

    function stopDrag() {
        dragging = false;
    }

    // Redraw when hue changes
    $effect(() => {
        drawGradient();
    });

    // Global drag handlers
    $effect(() => {
        document.addEventListener('mousemove', handleGlobalMove);
        document.addEventListener('mouseup', stopDrag);
        return () => {
            document.removeEventListener('mousemove', handleGlobalMove);
            document.removeEventListener('mouseup', stopDrag);
        };
    });
</script>

<div class="rounded-lg border bg-card p-6 shadow-sm">
    <div class="space-y-4">
        <!-- Header -->
        <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold">Color Picker</h3>
            <div class="flex items-center gap-2">
                <div class="size-6 rounded border shadow-sm" style="background-color: {hexColor};"></div>
                <code class="rounded bg-muted px-2 py-1 text-sm font-mono">{hexColor}</code>
            </div>
        </div>
        
        <!-- Picker -->
        <div class="flex gap-4">
            <canvas 
                bind:this={canvas}
                width={SIZE}
                height={SIZE}
                class="size-[200px] rounded-md border cursor-crosshair shadow-sm hover:shadow-md transition-shadow"
                onmousemove={getPixelColor}
            ></canvas>
            
            <div class="flex flex-col items-center gap-3">
                <div 
                    data-hue-slider
                    class="relative w-5 h-[200px] rounded-md border cursor-pointer select-none shadow-sm hover:shadow-md transition-all active:cursor-grabbing bg-[linear-gradient(to_bottom,#f00_0%,#ff0_17%,#0f0_33%,#0ff_50%,#00f_67%,#f0f_83%,#f00_100%)]"
                    onmousedown={startDrag}
                >
                    <div 
                        class="absolute -left-[3px] w-[26px] h-2.5 bg-background border-2 border-border rounded pointer-events-none shadow-md transition-all"
                        style="top: {(hue / 360) * SIZE - 5}px;"
                    ></div>
                </div>
            </div>
        </div>
    </div>
</div>