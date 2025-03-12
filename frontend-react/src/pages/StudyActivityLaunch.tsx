import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useNavigation } from "@/context/NavigationContext";
import { createStudySession } from "@/services/api";

type Group = {
  id: number;
  name: string;
};

type StudyActivity = {
  id: number;
  title: string;
  launch_url: string;
  preview_url: string;
};

type LaunchData = {
  activity: StudyActivity;
  groups: Group[];
};

export default function StudyActivityLaunch() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { setCurrentStudyActivity } = useNavigation();
  const [launchData, setLaunchData] = useState<LaunchData | null>(null);
  const [selectedGroup, setSelectedGroup] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/study-activities/${id}/launch`)
      .then((response) => {
        if (!response.ok) throw new Error("Failed to fetch launch data");
        return response.json();
      })
      .then((data) => {
        setLaunchData(data);
        setCurrentStudyActivity(data.activity);
        setLoading(false);

        // If activity id is not 1, launch immediately
        if (data.activity.id !== 1) {
          handleDirectLaunch(data.activity);
        }
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [id, setCurrentStudyActivity]);

  useEffect(() => {
    return () => {
      setCurrentStudyActivity(null);
    };
  }, [setCurrentStudyActivity]);

  const handleDirectLaunch = (activity: StudyActivity) => {
    window.open(activity.launch_url, "_blank");
    navigate("/");
  };

  const handleLaunch = async () => {
    if (!launchData?.activity || !selectedGroup) return;

    try {
      const result = await createStudySession(
        parseInt(selectedGroup),
        launchData.activity.id
      );
      console.log("createStudySession response:", result);

      // Extract session ID directly from session_id property
      const sessionId = result.session_id;
      if (!sessionId) {
        throw new Error("Session ID is missing in the response.");
      }
      const launchUrl = new URL(launchData.activity.launch_url);
      launchUrl.searchParams.set("group_id", selectedGroup);
      launchUrl.searchParams.set("session_id", sessionId.toString());

      window.open(launchUrl.toString(), "_blank");
      navigate(`/sessions/${sessionId}`);
    } catch (error) {
      console.error("Failed to launch activity:", error);
    }
  };

  if (loading) {
    return <div className="text-center">Loading...</div>;
  }

  if (error) {
    return <div className="text-red-500">Error: {error}</div>;
  }

  // If activity is not 1, we've already launched it.
  if (!launchData || launchData.activity.id !== 1) {
    return null;
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">{launchData.activity.title}</h1>

      <div className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">Select Word Group</label>
          <Select onValueChange={setSelectedGroup} value={selectedGroup}>
            <SelectTrigger>
              <SelectValue placeholder="Select a word group" />
            </SelectTrigger>
            <SelectContent>
              {launchData.groups.map((group) => (
                <SelectItem key={group.id} value={group.id.toString()}>
                  {group.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <Button
          onClick={handleLaunch}
          disabled={!selectedGroup}
          className="w-full"
        >
          Launch Now
        </Button>
      </div>
    </div>
  );
}
