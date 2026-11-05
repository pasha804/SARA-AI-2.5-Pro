// Pasha Nexus — Interactive Telemetry Engine
document.addEventListener("DOMContentLoaded", () => {
    initTelemetryGraph();
});

function initTelemetryGraph() {
    const canvas = document.getElementById("telemetryCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let points = [35, 42, 50, 48, 65, 78, 85, 92, 110, 125, 140, 148];
    let step = 0;

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Grid lines
        ctx.strokeStyle = "rgba(255, 255, 255, 0.04)";
        ctx.lineWidth = 1;
        for (let y = 30; y < canvas.height; y += 40) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
        }

        // Telemetry Curve
        ctx.beginPath();
        const dx = canvas.width / (points.length - 1);
        ctx.moveTo(0, canvas.height - points[0]);

        for (let i = 1; i < points.length; i++) {
            const x = i * dx;
            const y = canvas.height - (points[i] + Math.sin(step + i) * 3);
            ctx.lineTo(x, y);
        }

        // Gradient fill under curve
        ctx.strokeStyle = "#00f0ff";
        ctx.lineWidth = 2.5;
        ctx.stroke();

        ctx.lineTo(canvas.width, canvas.height);
        ctx.lineTo(0, canvas.height);
        ctx.closePath();

        const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
        grad.addColorStop(0, "rgba(0, 240, 255, 0.2)");
        grad.addColorStop(1, "rgba(0, 240, 255, 0.0)");
        ctx.fillStyle = grad;
        ctx.fill();

        step += 0.04;
        requestAnimationFrame(draw);
    }

    draw();
}

function triggerWorkflow(name) {
    alert(`[SARA Copilot]: Triggering autonomous workflow '${name}'...`);
}
