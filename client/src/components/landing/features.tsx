import { Eye, Map, FileText, Bot } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const features = [
  {
    icon: <Eye className="h-8 w-8" />,
    title: "AI Vision Analysis",
    description: "Our model analyzes your farmland photo to identify vegetation type, density, and health.",
    badge: "Gemini 1.5 Pro"
  },
  {
    icon: <Map className="h-8 w-8" />,
    title: "Location-Based Accuracy",
    description: "Integrates local weather and climate data to refine your carbon sequestration estimates.",
    badge: "Weather Integration"
  },
  {
    icon: <FileText className="h-8 w-8" />,
    title: "Professional Reports",
    description: "Generate comprehensive, shareable reports ready for certification programs and stakeholders.",
    badge: "GPT-4o Powered"
  },
  {
    icon: <Bot className="h-8 w-8" />,
    title: "Expert Chatbot",
    description: "Get instant answers to your questions about carbon credits and your analysis results.",
    badge: "AI Assistant"
  },
];

export function Features() {
  return (
    <section id="features" className="py-20 md:py-28 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl font-headline">
            Powered by Cutting-Edge AI
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-lg text-muted-foreground">
            We use a suite of advanced AI tools to give you the most accurate preliminary analysis possible.
          </p>
        </div>
        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature) => (
            <Card key={feature.title} className="flex flex-col text-left p-6 transition-all duration-300 hover:bg-accent/10 hover:-translate-y-2">
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 rounded-full bg-primary/10 text-primary">
                    {feature.icon}
                  </div>
                </div>
                <h3 className="text-xl font-bold font-headline">{feature.title}</h3>
                <p className="mt-2 text-muted-foreground flex-1">{feature.description}</p>
                <p className="mt-4 text-sm font-semibold text-accent">{feature.badge}</p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
