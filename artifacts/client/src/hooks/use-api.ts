import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useSite() {
  return useQuery({
    queryKey: ["site"],
    queryFn: api.getSite,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

export function usePosts() {
  return useQuery({
    queryKey: ["posts"],
    queryFn: api.getPosts,
    staleTime: 1000 * 60 * 5,
  });
}

export function usePost(slug: string) {
  return useQuery({
    queryKey: ["post", slug],
    queryFn: () => api.getPost(slug),
    staleTime: 1000 * 60 * 5,
    retry: false, // Don't retry on 404
  });
}
