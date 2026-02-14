'use client';

import { useState } from 'react';
import { useAuth, useUser } from '@clerk/nextjs';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Search, Star, Loader2 } from "lucide-react";

interface Paper {
    id: string;
    title: string;
    abstract: string;
    url?: string;
    similarity?: number;
}

export default function CalibrationPage() {
    const { isLoaded, userId, getToken } = useAuth();
    const { user } = useUser();
    const [query, setQuery] = useState('');
    const [papers, setPapers] = useState<Paper[]>([]);
    const [loading, setLoading] = useState(false);
    const [starred, setStarred] = useState<Set<string>>(new Set());

    const searchPapers = async () => {
        if (!query) return;
        setLoading(true);
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const res = await fetch(`${apiUrl}/api/v1/search?q=${encodeURIComponent(query)}&limit=10`);
            if (res.ok) {
                const data = await res.json();
                setPapers(data);
            }
        } catch (error) {
            console.error("Search failed", error);
        } finally {
            setLoading(false);
        }
    };

    const toggleStar = async (paper: Paper) => {
        console.log("Toggling star for:", paper.id);
        if (!userId) {
            console.error("No userId found. User might not be logged in.");
            return;
        }

        const newStarred = new Set(starred);
        const isStarring = !newStarred.has(paper.id);

        if (isStarring) {
            newStarred.add(paper.id);
        } else {
            newStarred.delete(paper.id);
        }
        setStarred(newStarred);

        // Optimistic UI update, then sync with backend
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            console.log("Sending interaction to:", `${apiUrl}/api/v1/interactions`);
            const res = await fetch(`${apiUrl}/api/v1/interactions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    paper_id: paper.id,
                    interaction_type: isStarring ? 'star' : 'unstar'
                }),
            });
            if (!res.ok) {
                const err = await res.text();
                throw new Error(`API Error: ${res.status} ${err}`);
            }
            console.log("Interaction success");
        } catch (error) {
            console.error("Interaction failed", error);
            // Revert if failed
            if (isStarring) newStarred.delete(paper.id);
            else newStarred.add(paper.id);
            setStarred(new Set(newStarred));
        }
    };

    if (!isLoaded) return <div className="flex justify-center p-10"><Loader2 className="animate-spin" /></div>;

    return (
        <div className="container mx-auto p-4 max-w-2xl">
            <div className="mb-8 text-center">
                <h1 className="text-2xl font-bold mb-2">Calibration</h1>
                <p className="text-gray-600">
                    Search for topics you are interested in and star relevant papers to build your profile.
                </p>
            </div>

            <div className="flex gap-2 mb-6">
                <Input
                    placeholder="e.g. 'self-supervised learning' or 'transformers'"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && searchPapers()}
                />
                <Button onClick={searchPapers} disabled={loading}>
                    {loading ? <Loader2 className="animate-spin" /> : <Search className="w-4 h-4" />}
                </Button>
            </div>

            <ScrollArea className="h-[600px] pr-4">
                <div className="space-y-4">
                    {papers.map((paper) => (
                        <Card key={paper.id} className="relative">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-lg leading-tight">
                                    <a href={paper.url} target="_blank" rel="noreferrer" className="hover:underline text-blue-600">
                                        {paper.title}
                                    </a>
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm text-gray-700 line-clamp-3 mb-3">{paper.abstract}</p>
                                <div className="flex justify-between items-center">
                                    <Badge variant="secondary">{(paper.similarity as number * 100).toFixed(0)}% Match</Badge>
                                    <Button
                                        variant={starred.has(paper.id) ? "default" : "outline"}
                                        size="sm"
                                        onClick={() => toggleStar(paper)}
                                    >
                                        <Star className={`w-4 h-4 mr-1 ${starred.has(paper.id) ? "fill-white" : ""}`} />
                                        {starred.has(paper.id) ? "Starred" : "Star"}
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                    {papers.length === 0 && !loading && query && (
                        <div className="text-center text-gray-500 py-10">No papers found. Try a different query.</div>
                    )}
                </div>
            </ScrollArea>
        </div>
    );
}
