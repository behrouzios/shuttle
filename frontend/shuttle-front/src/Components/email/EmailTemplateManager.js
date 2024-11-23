import React, { useState, useEffect } from "react";
import axios from "axios";

const EmailTemplateManager = () => {
  const [templates, setTemplates] = useState([]);
  const [formData, setFormData] = useState({
    id: null,
    name: "",
    subject: "",
    body: "",
  });
  const [isEditing, setIsEditing] = useState(false);
  const [message, setMessage] = useState("");
  const [selectedTemplate, setSelectedTemplate] = useState(""); // For bulk email
  const [bulkMessage, setBulkMessage] = useState(""); // For bulk email status
  const [bulkTaskId, setBulkTaskId] = useState(null); // Current task ID
  const [isTaskActive, setIsTaskActive] = useState(false); // Task status
  const [progress, setProgress] = useState(0); // Progress tracking

  const token = localStorage.getItem("authToken");

  // Fetch email templates
  const fetchTemplates = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/core/email-templates/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setTemplates(response.data);
    } catch (error) {
      console.error("Error fetching templates:", error);
      setMessage("Error fetching templates. Please try again later.");
    }
  };
  const fetchProgress = async () => {
    if (!bulkTaskId) return;

    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/core/bulk-email-progress/${bulkTaskId}/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setProgress(response.data.progress);
    } catch (error) {
      console.error("Error fetching progress:", error.response?.data || error);
    }
  };

  // Handle input changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle form submission (Create/Update template)
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isEditing) {
        await axios.put(
          `http://127.0.0.1:8000/core/email-templates/${formData.id}/`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        setMessage("Template updated successfully!");
      } else {
        await axios.post(
          "http://127.0.0.1:8000/core/email-templates/",
          formData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        setMessage("Template created successfully!");
      }
      fetchTemplates();
      setFormData({ id: null, name: "", subject: "", body: "" });
      setIsEditing(false);
    } catch (error) {
      console.error("Error submitting template:", error);
      setMessage("Error submitting template. Please try again.");
    }
  };

  // Handle edit button click
  const handleEdit = (template) => {
    setFormData(template);
    setIsEditing(true);
  };

  // Handle delete button click
  const handleDelete = async (id) => {
    try {
      await axios.delete(
        `http://127.0.0.1:8000/core/email-templates/${id}/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setMessage("Template deleted successfully!");
      fetchTemplates();
    } catch (error) {
      console.error("Error deleting template:", error);
      setMessage("Error deleting template.");
    }
  };

  // Handle bulk email start
  const handleSendBulkEmails = async () => {
    if (!selectedTemplate) {
      setBulkMessage("Please select a template to send bulk emails.");
      return;
    }
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/core/bulk-email-control/",
        { action: "start", template_name: selectedTemplate },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setBulkTaskId(response.data.task_id);
      setIsTaskActive(true);
      setBulkMessage("Bulk email task started successfully!");
    } catch (error) {
      console.error("Error sending bulk emails:", error.response?.data || error);
      setBulkMessage("Error sending bulk emails. Please try again.");
    }
  };

  // Handle bulk email pause
  const handlePause = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:8000/core/bulk-email-control/",
        { action: "pause", task_id: bulkTaskId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setIsTaskActive(false);
      setBulkMessage("Bulk email task paused successfully!");
    } catch (error) {
      console.error("Error pausing bulk emails:", error.response?.data || error);
      setBulkMessage("Error pausing bulk emails. Please try again.");
    }
  };

  // Handle bulk email resume
  const handleResume = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:8000/core/bulk-email-control/",
        { action: "resume", task_id: bulkTaskId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setIsTaskActive(true);
      setBulkMessage("Bulk email task resumed successfully!");
    } catch (error) {
      console.error("Error resuming bulk emails:", error.response?.data || error);
      setBulkMessage("Error resuming bulk emails. Please try again.");
    }
  };

  // Handle bulk email cancellation
  const handleCancel = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:8000/core/bulk-email-control/",
        { action: "cancel", task_id: bulkTaskId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setBulkTaskId(null);
      setIsTaskActive(false);
      setBulkMessage("Bulk email task canceled successfully!");
      setProgress(0); // Reset progress
    } catch (error) {
      console.error("Error canceling bulk emails:", error.response?.data || error);
      setBulkMessage("Error canceling bulk emails. Please try again.");
    }
  };

  // Poll for progress
  useEffect(() => {
    let progressInterval;

    if (bulkTaskId && isTaskActive) {
      progressInterval = setInterval(fetchProgress, 2000);
    }

    return () => {
      if (progressInterval) {
        clearInterval(progressInterval);
      }
    };
  }, [bulkTaskId, isTaskActive]);

  // Fetch templates on component mount
  useEffect(() => {
    fetchTemplates();
  }, []);

  return (
    <div>
      <h1>Email Template Manager</h1>
      {message && <p style={{ color: "green" }}>{message}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Template Name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="subject"
          placeholder="Template Subject"
          value={formData.subject}
          onChange={handleChange}
          required
        />
        <textarea
          name="body"
          placeholder="Template Body"
          value={formData.body}
          onChange={handleChange}
          required
        />
        <button type="submit">
          {isEditing ? "Update Template" : "Create Template"}
        </button>
      </form>

      <h2>Existing Templates</h2>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Name</th>
            <th>Subject</th>
            <th>Body</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {templates.length > 0 ? (
            templates.map((template) => (
              <tr key={template.id}>
                <td>{template.name}</td>
                <td>{template.subject}</td>
                <td>{template.body}</td>
                <td>
                  <button onClick={() => handleEdit(template)}>Edit</button>
                  <button onClick={() => handleDelete(template.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4">No templates available</td>
            </tr>
          )}
        </tbody>
      </table>

      <h2>Send Bulk Emails</h2>
      <div>
        <select
          value={selectedTemplate}
          onChange={(e) => setSelectedTemplate(e.target.value)}
        >
          <option value="">Select a Template</option>
          {templates.map((template) => (
            <option key={template.id} value={template.name}>
              {template.name}
            </option>
          ))}
        </select>
        <button onClick={handleSendBulkEmails}>Send Bulk Emails</button>
        {bulkMessage && <p style={{ color: "blue" }}>{bulkMessage}</p>}
        {bulkTaskId && (
          <div>
            <button onClick={isTaskActive ? handlePause : handleResume}>
              {isTaskActive ? "Pause" : "Resume"}
            </button>
            <button onClick={handleCancel}>Cancel</button>
          </div>
        )}
        {bulkTaskId && (
          <div>
            <h3>Progress: {progress}%</h3>
            <progress value={progress} max="100"></progress>
          </div>
        )}
      </div>
    </div>
  );
};

export default EmailTemplateManager;
