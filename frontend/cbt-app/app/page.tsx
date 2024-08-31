import Header from "@/components/Header";
import {
  Accessibility,
  Activity,
  Brain,
  ClipboardPlus,
  HeartPulse,
  Pill,
  PlusIcon,
} from "lucide-react";
import Image from "next/image";

export default function Home() {
  const features = [
    {
      name: "Secure Thought Journaling",
      description:
        "Confidentially record your thoughts and emotions to track your mental health progress.",
      icon: Accessibility,
    },
    {
      name: "Instant CBT Techniques",
      description:
        "Quickly access personalized cognitive-behavioral strategies to manage your mental well-being.",
      icon: Activity,
    },
    {
      name: "Session Summaries",
      description:
        "Review key insights and takeaways from your therapy sessions for ongoing reflection.",
      icon: Pill,
    },
    {
      name: "Mindfulness Exercises",
      description:
        "Engage with interactive mindfulness practices to enhance your self-awareness and relaxation.",
      icon: HeartPulse,
    },
    {
      name: "Cognitive Restructuring Tools",
      description:
        "Utilize cloud-based tools to identify and challenge negative thought patterns effectively.",
      icon: Brain,
    },
    {
      name: "Progressive Relaxation Guides",
      description:
        "Access guided techniques for muscle relaxation and stress reduction at your convenience.",
      icon: ClipboardPlus,
    },
  ];
  return (
    <main className="">
      <Header />
      <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-bl from-white to-red-500 p-4">
        <div className="max-auto max-w-2xl sm:text-center">
          <h2 className=" font-semibold leading-9 text-red-900 mt-11 text-center">
            MED-45 AI - Cognitive Behaviral Therapy
          </h2>
        </div>

        <p className="mt-6 text-lg text-center leading-8 text-red-900 max-auto max-w-2xl">
          Your Personalized Mental Health Companion
          <br />
          that responds to inquiries, summarizes information, and offers
          comprehensive insights in an interactive discussion, plus
          significantly galvanizes your mental health therapy session.
        </p>
        <div className="flex justify-center items-center mt-4">
          <div className="bg-gray-700 border btnStyle text-white p-2 rounded-md cursor-pointer">
            <p className="uppercase">Explore Miscellaneous Incentitives:</p>
          </div>
        </div>

        <div className="mx-auto mt-15 max-w-7xl px-6 sm:ml-20 md:mt-24">
          <dl className="mx-auto grid max-w-2xl grid-cols-1 gap-x-6 gap-y-10 text-base leading-7 sm:grid-cols-2 lg:mx-0 lg:max-w-none lg:grid-cols-3 lg:gap-x-8 lg:gap-y-16">
            {features.map((feature) => (
              <div key={feature.name} className="relative pl-9">
                <dt className="inline font-semibold text-gray-900">
                  <feature.icon
                    aria-hidden="true"
                    className="absolute left-1 top-1 h-5 w-5 text-black"
                  />
                </dt>
                <dd className="text-white bg-red-400/50 rounded-lg max-w-[300px] p-2">
                  {feature.description}
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </main>
  );
}
