'use client'

import Grid from '@mui/material/Grid';
import Image from 'next/image';
import MeteorContainer from '@/components/ui/meteors';

export default function HomePage () {
  return (
<Grid className="bg-base-100 dark:bg-black">
  <Grid container className="h-screen max-h-screen w-screen max-w-screen px-[16px] sm:px-[16px] md:px-[15vw] lg:px-[22.5vw] pt-[25vh] flex flex-col">
    <HomeContent />
  </Grid>
  <Footer />
</Grid>
  )};
  function HomeContent () {
    return (
<>
<div className="mb-8">
<span className="w-full flex justify-center mb-2">
<span className="text-6xl">🏞️</span>
</span>

<span className="w-full flex justify-center text-center">
<span className="aleo text-3xl font-light">Your <b>Natural Park</b> of <b>Python Utilities</b>.</span>
</span>
</div>

<div className="flex justify-center items-center w-full mb-4">
  <MeteorContainer text="pip install yosemite"></MeteorContainer>
</div>

<div className="flex flex-row space-x-6 justify-center items-center w-full">
  <button className="btn btn-ghost btn-disabled aleo">Explore | Coming Soon</button>
  <button onClick={() => window.open("/docs/index.html")} className="btn btn-outlined aleo">Documentation</button>
</div>
</>
    )};

function Footer () {
  return (
<Grid container className="fixed h-[15vh] w-screen bottom-0 flex flex-row justify-center items-center space-x-2">
<button className="btn btn-outlined flex items-center justify-center text-center w-[64px] h-[64px]">
  <Image src="/h.png" width="32" height="32" alt="H" />
</button>
<button className="btn btn-outlined flex items-center justify-center text-center w-[64px] h-[64px]">
  <i className="fi fi-brands-github text-2xl mt-2"></i>
</button>
<button className="btn btn-outlined flex items-center justify-center text-center w-[64px] h-[64px]">
  <i className="fi fi-brands-linkedin text-2xl mt-2"></i>
</button>
<button className="btn btn-outlined flex items-center justify-center text-center w-[64px] h-[64px]">
  <i className="fi fi-brands-spotify text-2xl mt-2"></i>
</button>
</Grid>
  )};