import React, { useEffect, useState } from "react";

const AccountsManagement = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch applications
  const fetchApplications = () => {
    const user = JSON.parse(localStorage.getItem("user"));
    const token = user?.token;

    if (!token) {
      setError("No access token found. Please log in.");
      setLoading(false);
      return;
    }

    setLoading(true);
    fetch("http://localhost:5000/api/admin/users?status=inProcess", {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    })
      .then(async (res) => {
        if (!res.ok) throw new Error(`Failed to fetch data: ${res.status}`);
        const contentType = res.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
          return res.json();
        } else {
          throw new Error("Expected JSON but got something else");
        }
      })
      .then((data) => {
        setApplications(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchApplications();
  }, []);

  // Function to update status
  const updateStatus = (userId, newStatus) => {
    const user = JSON.parse(localStorage.getItem("user"));
    const token = user?.token;

    if (!token) {
      setError("No access token found. Please log in.");
      return;
    }

    fetch(`http://localhost:5000/api/admin/users/${userId}/status`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ status: newStatus }),
    })
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to update status: ${res.status}`);
        return res.json();
      })
      .then(() => {
        // Option 1: Refetch the applications list from backend
        fetchApplications();

        // Option 2: Or update state locally for better UX:
        /*
        setApplications((prev) =>
          prev.filter((app) => app.id !== userId)
        );
        */
      })
      .catch((err) => {
        setError(err.message);
      });
  };

  if (loading) return <div className="p-8">Loading applications...</div>;
  if (error) return <div className="p-8 text-red-600">Error: {error}</div>;

  return (
    <div className="p-8 m-8 bg-white shadow-xl rounded-2xl border border-black max-w-6xl mx-auto">
      <h2 className="text-3xl font-bold mb-6">Applications List</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm border border-black rounded-xl">
          <thead className="bg-gray-100 border-b border-black">
            <tr>
              <th className="p-3 border border-black">Name</th>
              <th className="p-3 border border-black">Email Address</th>
              <th className="p-3 border border-black">Phone Number</th>
              <th className="p-3 border border-black">Country</th>
              <th className="p-3 border border-black">Registration Date</th>
              <th className="p-3 border border-black">Action</th>
            </tr>
          </thead>
          <tbody>
            {applications.length === 0 ? (
              <tr>
                <td colSpan="6" className="p-4 text-center">
                  No applications found.
                </td>
              </tr>
            ) : (
              applications.map((app, index) => (
                <tr key={app.id || index} className="text-center border-b border-black">
                  <td className="p-3 border border-black">{app.name}</td>
                  <td className="p-3 border border-black">{app.email}</td>
                  <td className="p-3 border border-black">{app.phoneNumber || "N/A"}</td>
                  <td className="p-3 border border-black">{app.country || "N/A"}</td>
                  <td className="p-3 border border-black">
                    {app.created_at ? app.created_at.split("T")[0] : "N/A"}
                  </td>
                  <td className="p-3 border border-black">
                    <div className="flex gap-2 justify-center">
                      <button
                        className="bg-black text-white px-3 py-1 rounded-full text-xs hover:bg-gray-800"
                        onClick={() => updateStatus(app.id, "approved")}
                      >
                        Approve
                      </button>
                      <button
                        className="bg-black text-white px-3 py-1 rounded-full text-xs hover:bg-gray-800"
                        onClick={() => updateStatus(app.id, "declined")}
                      >
                        Deny
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AccountsManagement;
