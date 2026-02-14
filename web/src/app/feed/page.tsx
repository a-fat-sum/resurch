'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@clerk/nextjs';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Star, Loader2, RefreshCw } from "lucide-react";

interface Paper {
    id: string;
    title: string;
    abstract: string;
    url?: string;
    similarity?: number;
}

export default function FeedPage() {
    const { isLoaded, userId } = useAuth();
    const [papers, setPapers] = useState<Paper[]>([]);
    const [loading, setLoading] = useState(false);
    const [starred, setStarred] = useState<Set<string>>(new Set());

    const fetchFeed = async () => {
        if (!userId) return;
        setLoading(true);
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const res = await fetch(`${apiUrl}/api/v1/feed?user_id=${userId}`);
            if (res.ok) {
                const data = await res.json();
                setPapers(data);
            }
        } catch (error) {
            console.error("Feed fetch failed", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (userId) {
            fetchFeed();
        }
    }, [userId]);

    const toggleStar = async (paper: Paper) => {
        if (!userId) return;

        const newStarred = new Set(starred);
        const isStarring = !newStarred.has(paper.id);

        if (isStarring) {
            newStarred.add(paper.id);
        } else {
            newStarred.delete(paper.id);
        }
        setStarred(newStarred);

        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            await fetch(`${apiUrl}/api/v1/interactions`, {
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
        } catch (error) {
            console.error("Interaction failed", error);
            if (isStarring) newStarred.delete(paper.id);
            else newStarred.add(paper.id);
            setStarred(new Set(newStarred));
        }
    };

    if (!isLoaded) return <div className="flex justify-center p-10"><Loader2 className="animate-spin" /></div>;

    return (
        <div className="container mx-auto p-4 max-w-2xl">
            <div className="mb-8 text-center">
                <h1 className="text-3xl font-bold mb-2">Your Feed</h1>
                <p className="text-gray-600 mb-4">
                    Personalized recommendations based on your starred papers.
                </p>
                <Button onClick={fetchFeed} variant="outline" size="sm" disabled={loading}>
                    <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                    Refresh Feed
                </Button>
            </div>

            <ScrollArea className="h-[700px] pr-4">
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
                    {papers.length === 0 && !loading && (
                        <div className="text-center text-gray-500 py-10">
                            No recommendations yet. Go to <a href="/calibration" className="text-blue-600 hover:underline">Calibration</a> to star more papers!
                        </div>
                    )}
                </div>
            </ScrollArea>
        </div>
    );
}
