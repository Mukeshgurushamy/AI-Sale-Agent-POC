import { useEffect, useRef, useState } from "react";
import "../styles/neural.css";

export default function NeuralHero({ hidden, pulseId }) {
  const canvasRef = useRef(null);
  const mouseRef = useRef({ x: null, y: null });
  const pulseRef = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    const nodes = Array.from({ length: 80 }).map(() => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3
    }));

    const onMouseMove = (e) => {
      mouseRef.current = { x: e.clientX, y: e.clientY };
    };

    window.addEventListener("mousemove", onMouseMove);

    function draw() {
      ctx.clearRect(0, 0, width, height);

      nodes.forEach((a, i) => {
        // Subtle attraction to mouse
        if (mouseRef.current.x !== null) {
          const dx = mouseRef.current.x - a.x;
          const dy = mouseRef.current.y - a.y;
          const dist = Math.sqrt(dx * dx + dy * dy) || 1;
          if (dist < 260) {
            const force = (1 - dist / 260) * 0.08;
            a.vx += dx * force * 0.002;
            a.vy += dy * force * 0.002;
          }          
        }

        a.x += a.vx;
        a.y += a.vy;

        if (a.x < 0 || a.x > width) a.vx *= -1;
        if (a.y < 0 || a.y > height) a.vy *= -1;

        nodes.slice(i).forEach(b => {
          const dx = a.x - b.x;
          const dy = a.y - b.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 140) {
            const intensity = Math.min(
                (1 - dist / 140) + pulseRef.current,
                1.5
              );              

            ctx.strokeStyle = `rgba(59,130,246,${intensity})`;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
        });
      });

      pulseRef.current *= 0.85;
      requestAnimationFrame(draw);
    }

    draw();

    window.onresize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };

    return () => {
      window.removeEventListener("mousemove", onMouseMove);
    };
  }, []);

  // Pulse when bot replies
  useEffect(() => {
    if (pulseId > 0) {
      pulseRef.current = 1.5;
    }
  }, [pulseId]);

  return (
    <div className={`neural-hero ${hidden ? "fade-out" : ""}`}>
      <canvas ref={canvasRef} />
      <div className="hero-content">
        <h1 className="morph-title">
          AI That Understands Your Leads
        </h1>
        <p>Real conversations. Real intent. Real conversions.</p>
      </div>
    </div>
  );
}
