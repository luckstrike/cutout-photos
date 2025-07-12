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

        // White to hue
        const horizontal = ctx.createLinearGradient(0, 0, 200, 0);
        horizontal.addColorStop(0, '#ffffff');
        horizontal.addColorStop(1, `hsl(${hue}, 100%, 50%)`);
        ctx.fillStyle = horizontal;
        ctx.fillRect(0, 0, 200, 200);

        // Transparent to black
        const vertical = ctx.createLinearGradient(0, 0, 0, 200);
        vertical.addColorStop(0, 'rgba(0,0,0,0)');
        vertical.addColorStop(1, 'rgba(0,0,0,1)');
        ctx.fillStyle = vertical;
        ctx.fillRect(0, 0, 200, 200);
    }

    function updateHue(event: MouseEvent) {
        const rect = event.currentTarget.getBoundingClientRect();
        const y = Math.max(0, Math.min(200, event.clientY - rect.top));
        hue = Math.round((y / 200) * 360);
    }

    function startDrag(event: MouseEvent) {
        dragging = true;
        updateHue(event);
    }

    $effect(() => {
        drawGradient();
        
        function handleMove(event: MouseEvent) {
            if (dragging) {
                const slider = document.querySelector('.hue-slider') as HTMLElement;
                if (slider) {
                    const rect = slider.getBoundingClientRect();
                    const y = Math.max(0, Math.min(200, event.clientY - rect.top));
                    hue = Math.round((y / 200) * 360);
                }
            }
        }
        
        function stopDrag() {
            dragging = false;
        }
        
        document.addEventListener('mousemove', handleMove);
        document.addEventListener('mouseup', stopDrag);
        
        return () => {
            document.removeEventListener('mousemove', handleMove);
            document.removeEventListener('mouseup', stopDrag);
        };
    });
</script>

<div class="flex flex-col gap-4 p-4">
    <div class="text-lg font-mono">{hexColor}</div>
    
    <div class="flex gap-4">
        <canvas 
            bind:this={canvas}
            width="200"
            height="200"
            class="border-2 border-gray-300 cursor-crosshair"
            style="width: 200px; height: 200px;"
            onmousemove={getPixelColor}
        ></canvas>
        
        <div class="flex flex-col items-center gap-2">
            <div 
                class="hue-slider"
                onmousedown={startDrag}
            >
                <div 
                    class="slider-thumb"
                    style="top: {(hue / 360) * 200 - 4}px;"
                ></div>
            </div>
        </div>
    </div>
</div>

<style>
    .hue-slider {
        position: relative;
        width: 20px;
        height: 200px;
        border: 2px solid #ccc;
        border-radius: 4px;
        cursor: pointer;
        user-select: none;
        background: linear-gradient(to bottom, 
            #ff0000 0%, #ffff00 16.66%, #00ff00 33.33%, 
            #00ffff 50%, #0000ff 66.66%, #ff00ff 83.33%, #ff0000 100%
        );
    }
    
    .hue-slider:active {
        cursor: grabbing;
    }
    
    .slider-thumb {
        position: absolute;
        left: -2px;
        width: 24px;
        height: 8px;
        background: white;
        border: 2px solid #333;
        border-radius: 2px;
        pointer-events: none;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }
</style>