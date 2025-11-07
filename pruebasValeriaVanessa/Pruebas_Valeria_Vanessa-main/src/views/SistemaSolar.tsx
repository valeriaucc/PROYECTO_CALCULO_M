import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

export default function SistemaSolar() {
  const mountRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const container = mountRef.current!;
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000010);

    const camera = new THREE.PerspectiveCamera(
      75,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 5, 35);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // ☀️ Sol
    const sunGeometry = new THREE.SphereGeometry(2.5, 64, 64);
    const sunMaterial = new THREE.MeshBasicMaterial({
      color: 0xffdd33,
      emissive: 0xffaa00,
    });
    const sun = new THREE.Mesh(sunGeometry, sunMaterial);
    scene.add(sun);

    // 💡 Luz del Sol
    const sunLight = new THREE.PointLight(0xffffff, 3.5, 200);
    scene.add(sunLight);

    // 🌌 Fondo de estrellas
    const starGeometry = new THREE.BufferGeometry();
    const starCount = 2000;
    const starPositions = new Float32Array(starCount * 3);
    for (let i = 0; i < starCount * 3; i++) {
      starPositions[i] = (Math.random() - 0.5) * 800;
    }
    starGeometry.setAttribute(
      "position",
      new THREE.BufferAttribute(starPositions, 3)
    );
    const starMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 0.7 });
    const stars = new THREE.Points(starGeometry, starMaterial);
    scene.add(stars);

    // 🌍 Planetas
    const planetData = [
      { name: "Mercurio", color: 0xb1b1b1, size: 0.4, distance: 4, speed: 0.025, angle: 0 },
      { name: "Venus", color: 0xffc04d, size: 0.7, distance: 7, speed: 0.018, angle: 0 },
      { name: "Tierra", color: 0x1e90ff, size: 0.75, distance: 10, speed: 0.012, angle: 0 },
      { name: "Marte", color: 0xff4500, size: 0.6, distance: 13, speed: 0.009, angle: 0 },
      { name: "Júpiter", color: 0xffe4b5, size: 1.5, distance: 17, speed: 0.007, angle: 0 },
      { name: "Saturno", color: 0xf5deb3, size: 1.2, distance: 21, speed: 0.006, angle: 0 },
      { name: "Urano", color: 0x40e0d0, size: 1.0, distance: 25, speed: 0.004, angle: 0 },
      { name: "Neptuno", color: 0x4169e1, size: 1.0, distance: 29, speed: 0.003, angle: 0 },
    ];

    const planets = planetData.map((p) => {
      const geo = new THREE.SphereGeometry(p.size, 32, 32);
      const mat = new THREE.MeshPhongMaterial({
        color: p.color,
        emissive: p.color,
        emissiveIntensity: 0.4,
        shininess: 80,
      });
      const mesh = new THREE.Mesh(geo, mat);
      scene.add(mesh);
      return { ...p, mesh };
    });

    // 🪐 Anillos de Saturno
    const saturn = planets.find((p) => p.name === "Saturno");
    if (saturn) {
      const ringGeometry = new THREE.RingGeometry(1.6, 2.3, 64);
      const ringMaterial = new THREE.MeshBasicMaterial({
        color: 0xd2b48c,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.7,
      });
      const ring = new THREE.Mesh(ringGeometry, ringMaterial);
      ring.rotation.x = Math.PI / 2;
      saturn.mesh.add(ring);
    }

    // 🎮 Controles interactivos
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.enableZoom = true;
    controls.target.set(0, 0, 0);
    controls.update();

    // 🚀 Animación
    const animate = () => {
      requestAnimationFrame(animate);
      sun.rotation.y += 0.004;

      planets.forEach((p) => {
        p.angle += p.speed;
        p.mesh.position.set(
          Math.cos(p.angle) * p.distance,
          0,
          Math.sin(p.angle) * p.distance
        );
        p.mesh.rotation.y += 0.02;
      });

      stars.rotation.y += 0.0005;
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // 📏 Redimensionamiento
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
  }, []);

  return (
    <div className="relative w-full h-screen overflow-hidden">
      {/* 🌌 Fondo degradado tipo espacio */}
      <div className="absolute inset-0 bg-gradient-to-b from-indigo-900 via-black to-blue-900"></div>

      {/* 🪐 Contenedor 3D */}
      <div
        ref={mountRef}
        className="absolute inset-0 w-full h-full flex items-center justify-center"
      ></div>

    </div>
  );
}
