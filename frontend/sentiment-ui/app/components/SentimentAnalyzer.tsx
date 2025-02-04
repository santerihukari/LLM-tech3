"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function SentimentAnalyzer() {
  const [text, setText] = useState<string>("");
  const [model, setModel] = useState<string>("custom");
  const [result, setResult] = useState<{ sentiment: string; confidence?: number } | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const analyzeSentiment = async () => {
    if (!text) return;
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, model }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error analyzing sentiment:", error);
      setResult({ sentiment: "Error", confidence: undefined });
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center space-y-4 p-6 max-w-md mx-auto">
      <Card className="w-full p-4">
        <CardHeader>
          <CardTitle>Sentiment Analyzer</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input
            placeholder="Enter text here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <Select onValueChange={setModel} defaultValue={model}>
            <SelectTrigger>
              <SelectValue placeholder="Select a model" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="custom">Custom Model</SelectItem>
              <SelectItem value="llama">Llama 3</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={analyzeSentiment} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Sentiment"}
          </Button>
        </CardContent>
      </Card>
      {result && (
        <Card className="w-full p-4">
          <CardHeader>
            <CardTitle>Result</CardTitle>
          </CardHeader>
          <CardContent>
            <p>Sentiment: <strong>{result.sentiment}</strong></p>
            {result.confidence !== undefined && (
              <p>Confidence: <strong>{result.confidence}</strong></p>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
