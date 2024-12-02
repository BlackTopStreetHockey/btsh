"use client"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function Register() {
  const [formData, setFormData] = useState({
    email: "",
    signature: ""
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // Handle form submission
    console.log("Form submitted:", formData)
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <h1 className="text-3xl font-bold mb-8">2024 BTSH Registration</h1>
      
      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">REGISTRATION & WAIVER 2024</h2>
        
        <div className="bg-yellow-50 p-4 rounded-lg mb-6">
          <p className="font-medium">
            BLACK TOP STREET HOCKEY, INC. OF NEW YORK CITY LIABILITY WAIVER and 
            SPORTSMANSHIP AND FAIR PLAY AGREEMENT RELEASE OF LIABILITY, WAIVER OF 
            CLAIMS, ASSUMPTION OF RISKS AND INDEMNITY AGREEMENT.
          </p>
          <p className="mt-2 text-red-600">
            BY COMPLETING THIS DOCUMENT YOU WILL WAIVE CERTAIN LEGAL RIGHTS, 
            INCLUDING THE RIGHT TO SUE. PLEASE READ THIS CONTRACT CAREFULLY.
          </p>
        </div>

        <p className="mb-4">
          <strong>Group Organizer&apos;s Name:</strong> Black Top Street Hockey, Inc, 
          and all of its recognized programs, hereinafter to be referred to as &quot;BTSH.&quot;
        </p>

        <p className="mb-4">
          <strong>TO:</strong> BTSH, Inc. and all of its recognized programs:
        </p>
      </section>

      <section className="mb-8">
        <h3 className="text-xl font-semibold mb-4">ASSUMPTION OF RISKS:</h3>
        <p className="mb-4">
          I am aware that participating in the activities and sports, without limitation, 
          offered by or associated with BTSH, exposes me to many inherent risks, dangers 
          and hazards. By engaging in any activities offered by or associated with BTSH, 
          I freely accept and fully assume all inherent risks, dangers and hazards and 
          the possibility of personal injury, death, property damage or loss resulting there from.
        </p>
      </section>

      <section className="mb-8">
        <h3 className="text-xl font-semibold mb-4">
          RELEASE OF LIABILITY WAIVER OF CLAIMS & INDEMNITY AGREEMENT:
        </h3>
        <p className="mb-4">
          In consideration of BTSH permitting me to participate in its activities and sports, 
          permitting me to the use of its equipment and permitting me the use of its facilities, 
          I hereby agree as follows:
        </p>

        <ol className="list-decimal pl-6 space-y-4">
          <li>
            TO WAIVE ANY AND ALL CLAIMS that I have or may in the future have against BTSH, 
            and its directors, officers, employees, agents, representatives, assigns and successors.
          </li>
          <li>
            TO RELEASE BTSH, and its directors, officers, employees, agents, representatives, 
            assigns and successors from any and all liability for any loss, damage, injury or 
            expense that I may suffer or that my next of kin may suffer, as a result of my 
            participation in activities and sports offered by BTSH, due to any cause whatsoever 
            INCLUDING NEGLIGENCE, BREACH OF CONTRACT, AND BREACH OF STATUTORY DUTY OF CARE ON 
            THE PART OF BTSH and its directors, officers, employees, agents, representatives, 
            assigns and successors.
          </li>
          <li>
            TO HOLD HARMLESS AND INDEMNIFY BTSH, and directors, officers, employees, agents, 
            representatives, assigns and successors from any and all liability for any property 
            damage or personal injury to any third party, resulting from my activities and my 
            participation in the activities offered by or associated with BTSH.
          </li>
          <li>
            That this Agreement shall be effecting and binding upon any heirs, next of kin, 
            executors, administrators and assigns in the event of my death.
          </li>
          <li>
            I have read and understood this Agreement prior to submitting, signing or emailing it. 
            I am aware that by either submitting, signing OR emailing this Agreement, I am waiving 
            certain legal rights which I or any heirs, next of kin, executors, administrators and 
            assigns may have against BTSH and its directors, officers, employees, agents, 
            representatives, assigns and successors.
          </li>
          <li>
            I affirm that I am 18 years of age or older.
          </li>
        </ol>
      </section>

      <section className="mb-8">
        <h3 className="text-xl font-semibold mb-4">SPORTSMANSHIP AND FAIR PLAY</h3>
        <ol className="list-[lower-alpha] pl-6 space-y-4">
          <li>
            I have read, understand and will abide by the rules of the BTSH program or 
            league for which I&apos;m registering.
          </li>
          <li>
            I understand that I am responsible for my own fouls and behavior.
          </li>
          <li>
            I understand that if it is reported by a referee, league official or an opponent 
            that I have behaved in an unsportsmanlike manner or have not played by the rules 
            that I could be suspended or expelled from the league with no refund.
          </li>
          <li>
            I understand that my team captain is the only person from my team who can approach 
            and address a referee or the opposing captain during a game. It is my responsibility 
            to let my captain know of my concerns so he or she can appropriately address the concerns.
          </li>
        </ol>
      </section>

      <form onSubmit={handleSubmit} className="space-y-6 mt-8 border-t pt-8">
        <div className="space-y-2">
          <Label htmlFor="email">Email Address</Label>
          <Input
            id="email"
            type="email"
            placeholder="your.email@example.com"
            required
            value={formData.email}
            onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
            className="max-w-md"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="signature">
            Digital Signature 
            <span className="text-sm text-muted-foreground ml-2">
              (Type your full legal name)
            </span>
          </Label>
          <Input
            id="signature"
            type="text"
            placeholder="Full Legal Name"
            required
            value={formData.signature}
            onChange={(e) => setFormData(prev => ({ ...prev, signature: e.target.value }))}
            className="max-w-md"
          />
        </div>

        <div className="pt-4">
          <Button type="submit" size="lg">
            Next
          </Button>
        </div>

        <p className="text-sm text-muted-foreground mt-4">
          By clicking Next, you acknowledge that you have read and agree to the terms 
          outlined in this waiver.
        </p>
      </form>
    </div>
  )
}

