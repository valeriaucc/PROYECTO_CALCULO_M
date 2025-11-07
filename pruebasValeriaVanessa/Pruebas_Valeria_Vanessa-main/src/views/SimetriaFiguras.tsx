import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

export default function SimetriaFiguras() {
  const mountRef = useRef<HTMLDivElement | null>(null);
  const [figuraSeleccionada, setFiguraSeleccionada] = useState("Cubo");

  useEffect(() => {
    const container = mountRef.current!;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      75,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 2, 6);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    scene.add(new THREE.AmbientLight(0xffffff, 0.6));
    const pointLight = new THREE.PointLight(0xffffff, 1);
    pointLight.position.set(5, 5, 5);
    scene.add(pointLight);

    const crearFigura = (tipo: string) => {
      switch (tipo) {
        case "Cubo":
          return new THREE.BoxGeometry(1, 1, 1);
        case "Pirámide":
          return new THREE.ConeGeometry(1, 1.5, 4);
        case "Pentágono":
          return new THREE.CylinderGeometry(0, 1, 1.2, 5);
        case "Estrella":
          const shape = new THREE.Shape();
          const spikes = 5;
          const outerRadius = 1;
          const innerRadius = 0.4;
          for (let i = 0; i < spikes * 2; i++) {
            const radius = i % 2 === 0 ? outerRadius : innerRadius;
            const angle = (i * Math.PI) / spikes;
            const x = Math.cos(angle) * radius;
            const y = Math.sin(angle) * radius;
            i === 0 ? shape.moveTo(x, y) : shape.lineTo(x, y);
          }
          shape.closePath();
          return new THREE.ExtrudeGeometry(shape, { depth: 0.3, bevelEnabled: false });
        case "Corazón":
          const heart = new THREE.Shape();
          heart.moveTo(0, 0);
          heart.bezierCurveTo(0, 1, -1, 1.5, -1.5, 1);
          heart.bezierCurveTo(-2.5, 0, 0, -1.5, 0, -1.5);
          heart.bezierCurveTo(0, -1.5, 2.5, 0, 1.5, 1);
          heart.bezierCurveTo(1, 1.5, 0, 1, 0, 0);
          return new THREE.ExtrudeGeometry(heart, { depth: 0.3, bevelEnabled: false });
        default:
          return new THREE.BoxGeometry(1, 1, 1);
      }
    };

    const geometry = crearFigura(figuraSeleccionada);
    const materialOriginal = new THREE.MeshStandardMaterial({ color: 0x66ccff });
    const materialReflejo = new THREE.MeshStandardMaterial({
      color: 0xff66cc,
      opacity: 0.8,
      transparent: true,
    });

    const original = new THREE.Mesh(geometry, materialOriginal);
    const reflejo = new THREE.Mesh(geometry, materialReflejo);

    original.position.x = -1.5;
    reflejo.position.x = 1.5;
    reflejo.scale.x *= -1;

    scene.add(original, reflejo);

    const plano = new THREE.Mesh(
      new THREE.PlaneGeometry(0.05, 5),
      new THREE.MeshBasicMaterial({ color: 0x444444 })
    );
    scene.add(plano);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    const animate = () => {
      requestAnimationFrame(animate);
      original.rotation.y += 0.01;
      reflejo.rotation.y -= 0.01;
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    };
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      container.removeChild(renderer.domElement);
    };
  }, [figuraSeleccionada]);

  return (
    <div className="w-full h-screen flex flex-col items-center justify-center bg-gradient-to-br from-pink-100 via-violet-100 to-sky-100">
      <select
        value={figuraSeleccionada}
        onChange={(e) => setFiguraSeleccionada(e.target.value)}
        className="mb-6 px-4 py-2 rounded-lg border-2 border-pink-300 bg-white text-pink-700 font-semibold shadow-sm hover:border-violet-500 transition"
      >
        <option>Cubo</option>
        <option>Pirámide</option>
        <option>Pentágono</option>
        <option>Estrella</option>
        <option>Corazón</option>
      </select>

      <div
        ref={mountRef}
        className="w-[600px] h-[400px] mx-auto bg-transparent"
      ></div>
    </div>
  );
}
