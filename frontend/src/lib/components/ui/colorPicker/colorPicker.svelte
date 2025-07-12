<script lang="ts">
    let canvas: HTMLCanvasElement;
    let hexColor = $state("#0000ff");
    let hue = $state(240);
    let dragging = $state(false);

    function getPixelColor(event: MouseEvent) {
        const ctx = canvas.getContext('2d')!;
        const [r, g, b] = ctx.getImageData(event.offsetX, event.offsetY, 1, 1).data;
        hexColor = `#${[r, g, b].map(c => c.toString(16).padStart(2, '0')).join('')}`;
    }

    function drawGradient() {
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d')!;
        ctx.clearRect(0, 0, 200, 200);

        // White to hue gradient
        const horizontal = ctx.createLinearGradient(0, 0, 200, 0);
        horizontal.addColorStop(0, '#ffffff');
        horizontal.addColorStop(1, `hsl(${hue}, 100%, 50%)`);
        ctx.fillStyle = horizontal;
        ctx.fillRect(0, 0, 200, 200);

        // Transparent to black gradient
        const vertical = ctx.createLinearGradient(0, 0, 0, 200);
        vertical.addColorStop(0, 'rgba(0,0,0,0)');
        vertical.addColorStop(1, 'rgba(0,0,0,1)');
        ctx.fillStyle = vertical;
        ctx.fillRect(0, 0, 200, 200);
    }

    function startDrag(event: MouseEvent) {
        dragging = true;
        const rect = event.currentTarget.getBoundingClientRect();
        const y = Math.max(0, Math.min(200, event.clientY - rect.top));
        hue = Math.round((y / 200) * 360);
    }

    $effect(() => {
        drawGradient();
        
        function handleMove(event: MouseEvent) {
            if (!dragging) return;
            const slider = document.querySelector('[data-hue-slider]') as HTMLElement;
            if (slider) {
                const rect = slider.getBoundingClientRect();
                const y = Math.max(0, Math.min(200, event.clientY - rect.top));
                hue = Math.round((y / 200) * 360);
            }
        }
        
        function stopDrag() { dragging = false; }
        
        document.addEventListener('mousemove', handleMove);
        document.addEventListener('mouseup', stopDrag);
        
        return () => {
            document.removeEventListener('mousemove', handleMove);
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
                <div 
                    class="h-6 w-6 rounded border shadow-sm" 
                    style="background-color: {hexColor};"
                ></div>
                <code class="rounded bg-muted px-2 py-1 text-sm font-mono">{hexColor}</code>
            </div>
        </div>
        
        <!-- Picker Area -->
        <div class="flex gap-4">
            <!-- Color Canvas -->
            <canvas 
                bind:this={canvas}
                width="200"
                height="200"
                class="size-[200px] rounded-md border cursor-crosshair shadow-sm hover:shadow-md transition-shadow"
                onmousemove={getPixelColor}
            ></canvas>
            
            <!-- Hue Slider -->
            <div class="flex flex-col items-center gap-3">
                <div 
                    data-hue-slider
                    class="relative w-5 h-[200px] rounded-md border cursor-pointer select-none shadow-sm hover:shadow-md transition-all active:cursor-grabbing bg-[linear-gradient(to_bottom,#ff0000_0%,#ffff00_16.66%,#00ff00_33.33%,#00ffff_50%,#0000ff_66.66%,#ff00ff_83.33%,#ff0000_100%)]"
                    onmousedown={startDrag}
                >
                    <!-- Slider Thumb -->
                    <div 
                        class="absolute -left-[3px] w-[26px] h-[10px] bg-background border-2 border-border rounded pointer-events-none shadow-md transition-all hover:border-ring hover:shadow-lg"
                        style="top: {(hue / 360) * 200 - 5}px;"
                    ></div>
                </div>
                <span class="text-xs text-muted-foreground font-medium">{hue}°</span>
            </div>
        </div>
    </div>
</div>