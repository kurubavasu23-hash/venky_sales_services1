import { Canvas, useFrame } from '@react-three/fiber';
import { Environment, Float, RoundedBox } from '@react-three/drei';
import { useRef } from 'react';

function Lens({ position, size = 0.105 }) {
  return <group position={position} rotation={[Math.PI / 2, 0, 0]}>
    <mesh><cylinderGeometry args={[size, size, 0.035, 40]} /><meshStandardMaterial color="#111318" metalness={0.82} roughness={0.24} /></mesh>
    <mesh position={[0, 0.02, 0]}><circleGeometry args={[size * 0.68, 32]} /><meshPhysicalMaterial color="#102232" metalness={0.45} roughness={0.13} clearcoat={1} /></mesh>
    <mesh position={[0, 0.023, 0]}><circleGeometry args={[size * 0.32, 32]} /><meshBasicMaterial color="#8197a4" transparent opacity={0.36} /></mesh>
  </group>;
}

function Device({ rear = false }) {
  return <group rotation={rear ? [0, Math.PI, 0] : [0, 0, 0]}>
    <RoundedBox args={[1.48, 3.02, 0.16]} radius={0.22} smoothness={10}>
      <meshStandardMaterial color="#77716a" metalness={0.92} roughness={0.2} />
    </RoundedBox>
    <RoundedBox position={[0, 0, rear ? -0.084 : 0.084]} args={[1.405, 2.945, 0.035]} radius={0.2} smoothness={10}>
      <meshPhysicalMaterial color={rear ? '#111318' : '#070a0f'} metalness={rear ? 0.7 : 0.35} roughness={0.16} clearcoat={1} clearcoatRoughness={0.08} />
    </RoundedBox>
    {rear ? <>
      <RoundedBox position={[-0.39, 1.03, -0.11]} args={[0.43, 0.74, 0.045]} radius={0.1} smoothness={8}>
        <meshStandardMaterial color="#25272a" metalness={0.72} roughness={0.22} />
      </RoundedBox>
      <Lens position={[-0.39, 1.25, -0.15]} size={0.09} />
      <Lens position={[-0.39, 1.01, -0.15]} size={0.09} />
      <Lens position={[-0.39, 0.77, -0.15]} size={0.07} />
      <mesh position={[-0.1, 0, -0.106]}><circleGeometry args={[0.19, 40]} /><meshStandardMaterial color="#191b1e" metalness={0.62} roughness={0.3} /></mesh>
      <mesh position={[-0.1, 0, -0.109]}><circleGeometry args={[0.14, 40]} /><meshStandardMaterial color="#26282b" metalness={0.62} roughness={0.26} /></mesh>
      <mesh position={[0.58, 0.91, -0.11]}><circleGeometry args={[0.055, 32]} /><meshBasicMaterial color="#e5e1d3" /></mesh>
    </> : <>
      <RoundedBox position={[0, 0, 0.106]} args={[1.33, 2.83, 0.027]} radius={0.17} smoothness={10}>
        <meshPhysicalMaterial color="#0b1420" metalness={0.22} roughness={0.1} clearcoat={1} clearcoatRoughness={0.04} />
      </RoundedBox>
      <mesh position={[0, 0.2, 0.123]}><planeGeometry args={[1.22, 2.28]} /><meshBasicMaterial color="#111c2a" /></mesh>
      <mesh position={[0, 0.7, 0.126]}><circleGeometry args={[0.54, 64]} /><meshBasicMaterial color="#b99a55" transparent opacity={0.13} /></mesh>
      <mesh position={[0, -0.25, 0.127]}><circleGeometry args={[0.69, 64]} /><meshBasicMaterial color="#6a7b93" transparent opacity={0.14} /></mesh>
      <mesh position={[0, 1.27, 0.13]}><capsuleGeometry args={[0.055, 0.15, 6, 16]} /><meshBasicMaterial color="#020304" /></mesh>
      <mesh position={[-0.73, 0.45, 0]}><boxGeometry args={[0.025, 0.42, 0.07]} /><meshStandardMaterial color="#bca56b" metalness={0.94} roughness={0.17} /></mesh>
      <mesh position={[0.73, 0.56, 0]}><boxGeometry args={[0.025, 0.57, 0.07]} /><meshStandardMaterial color="#bca56b" metalness={0.94} roughness={0.17} /></mesh>
    </>}
  </group>;
}

function Pair() {
  const ref = useRef();
  useFrame(({ clock }) => {
    if (ref.current) {
      ref.current.rotation.y = Math.sin(clock.elapsedTime * 0.28) * 0.075 - 0.15;
      ref.current.rotation.x = Math.sin(clock.elapsedTime * 0.22) * 0.025;
    }
  });
  return <group ref={ref}>
    <group position={[-0.22, -0.02, 0.28]} rotation={[0, 0, -0.1]}><Device /></group>
    <group position={[0.64, -0.08, -0.45]} scale={0.96} rotation={[0, -0.36, 0.08]}><Device rear /></group>
  </group>;
}

export default function ProductScene() {
  return <div className="three-canvas"><Canvas camera={{ position: [0, 0, 7.1], fov: 34 }} dpr={[1, 1.35]} gl={{ alpha: true, antialias: true }}>
    <ambientLight intensity={1.55} />
    <spotLight position={[4, 6, 5]} intensity={48} angle={0.55} penumbra={0.8} color="#ffe7aa" />
    <pointLight position={[-3, -1, 2]} intensity={16} color="#d4af37" />
    <pointLight position={[3, 1, -3]} intensity={20} color="#8da6cb" />
    <Environment preset="studio" />
    <Float speed={1.25} rotationIntensity={0.035} floatIntensity={0.16}><Pair /></Float>
  </Canvas><div className="hero-device-glow" /></div>;
}
