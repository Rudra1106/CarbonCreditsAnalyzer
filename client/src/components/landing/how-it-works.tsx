import { Upload, MapPin, BarChart2 } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const steps = [
  {
    icon: <Upload className="h-10 w-10 text-primary" />,
    title: "Upload Farmland Photo",
    description: "Drag and drop or select a clear image of your land. Our AI gets to work instantly.",
  },
  {
    icon: <MapPin className="h-10 w-10 text-primary" />,
    title: "Add Your Location",
    description: "Optionally provide your city and state to factor in local climate data for a more accurate result.",
  },
  {
    icon: <BarChart2 className="h-10 w-10 text-primary" />,
    title: "Get Instant Analysis",
    description: "Receive a detailed report on your carbon credit potential, revenue estimates, and expert advice.",
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="py-20 md:py-28">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl font-headline">
            Three Simple Steps to Insight
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-lg text-muted-foreground">
            From photo to full report in under a minute.
          </p>
        </div>
        <div className="grid gap-8 md:grid-cols-3">
          {steps.map((step, index) => (
            <Card key={index} className="text-center bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardHeader>
                <div className="flex justify-center mb-4">{step.icon}</div>
                <CardTitle className="font-headline">{step.title}</CardTitle>
                <CardDescription className="mt-2 text-base">{step.description}</CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
