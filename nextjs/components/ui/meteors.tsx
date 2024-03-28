'use client'

import { cn } from "@/utils/cn";
import clsx from "clsx";
import React from "react";

import { useState } from "react";
import Grid from '@mui/material/Grid';
import { Toaster, toast } from 'sonner';

export const Meteors = ({
  number,
  className,
}: {
  number?: number;
  className?: string;
}) => {
  const meteors = new Array(number || 20).fill(true);
  return (
    <>
      {meteors.map((el, idx) => (
        <span
          key={"meteor" + idx}
          className={cn(
            "animate-meteor-effect absolute top-1/2 left-1/2 h-0.5 w-0.5 rounded-[9999px] bg-sky-100 shadow-[0_0_0_1px_#ffffff10] rotate-[215deg]",
            "before:content-[''] before:absolute before:top-1/2 before:transform before:-translate-y-[50%] before:w-[50px] before:h-[1px] before:bg-gradient-to-r before:from-[#64748b] before:to-transparent",
            className
          )}
          style={{
            top: 0,
            left: Math.floor(Math.random() * (400 - -400) + -400) + "px",
            animationDelay: Math.random() * (0.8 - 0.2) + 0.2 + "s",
            animationDuration: Math.floor(Math.random() * (10 - 2) + 2) + "s",
          }}
        ></span>
      ))}
    </>
  );
};

export default function MeteorContainer({ text }: { text: string }) {
    const [hovered, setHovered] = useState(false);
      return (
        <>
          <Toaster />
          <Grid container className="flex justify-center">
            <div
            onMouseOver={() => setHovered(true)}
            onMouseOut={() => setHovered(false)}
              onClick={() => {
                if (!navigator.clipboard) {
                  toast.error('Clipboard functionality not available.');
                  return;
                }
    
                navigator.clipboard.writeText(text)
                  .then(() => {
                    toast.success('Copied to clipboard!');
                  })
                  .catch(err => {
                    console.error('Could not copy text: ', err);
                    toast.error('Failed to copy to clipboard.');
                  });
              }}
              className="relative inline-block group"
            >
              <div className={`border bg-black border-slate-800 rounded-2xl overflow-hidden ease-in-out duration-300 transition-all ${hovered ? 'shadow-xl' : 'shadow-sm'}`}>
                <div className="px-4 py-4 relative">
                  <pre className="text-sm bg-gray-900 rounded-lg p-4 relative">
                    <code className={`text-white jet ${hovered ? 'font-bold' : 'font-medium'}`}>
                        {text}</code>
                    <div className="absolute inset-0 pointer-events-none">
                      <Meteors number={20} />
                    </div>
                  </pre>
                  <button className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity duration-300">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="h-5 w-5 text-gray-400 hover:text-gray-200"
                    >
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </Grid>
        </>
      );
    }