"use client"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function RegisterationStep() {


    return (
        <div>
            <h1>Full Name</h1>
            <p>*</p>
            <h1>Gender</h1>
            <p>*</p>
            <h1>Female</h1>
Male
            <h1>Non-binary</h1>
            <h1>What position do you play?</h1>
            <p>*</p>
            <li>Defense</li>
            <li>Forward</li>
            <li>Goalie</li>
            
            <h1>2024 BTSH Team</h1>
            <p>*</p>
            <h1>Where do you live?</h1>
            <p>*</p>
            <h1>I care about the League and am interested in helping out with (check all that apply):</h1>
            <p>*</p>
            <h1>Reffing (paid)</h1>
            <h1>Opening/Closing (paid)</h1>
Some other capacity that I'm good at (handyperson skills, web design, etc.) Add your answer in the next question below.
            <h1>Sorry, maybe next year.</h1>
            <h1>I’d like to help! I’m good at:</h1>
            <h1>Theme ideas for the 2024 mid-season party?!</h1>
        </div>
    )
}