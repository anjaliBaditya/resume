import React, { useState } from 'react';

export default function FormGen() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    education: '',
    experience1: '',
    experience1_highlights: '',
    experience2: '',
    experience2_highlights: '',
    experience3: '',
    experience3_highlights: '',
    skills: '',
    githubLink: '',
    linkedinLink: '',
    personalWebsite: '',
    projectTitle: '',
    projectDescription: '',
    projectChoice: 'file', // Default choice is 'file'
    projectFile: null, // Remove this line if no longer needed
    projectGithub: '', // Use an empty string for the link
    projectLink: '' // Use an empty string for the link
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('/api/generate-resume', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });
    const result = await response.json();
    
    // Open PDF in a new tab
    window.open(result.pdfFilePath, '_blank');
  };

  return (
    <div className="max-w-lg mx-auto p-5">
      <h1 className="text-2xl font-bold mb-5">Resume Builder</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Name */}
        <div>
          <label className="block mb-2 font-medium">
            Name:
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            />
          </label>
        </div>

        {/* Email */}
        <div>
          <label className="block mb-2 font-medium">
            Email:
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            />
          </label>
        </div>

        {/* Phone */}
        <div>
          <label className="block mb-2 font-medium">
            Phone:
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            />
          </label>
        </div>

        

        {/* Experience 2 */}
        <div>
          <label className="block mb-2 font-medium">
            Experience 2 (Company Name):
            <textarea
              name="experience2"
              placeholder='Enter company name'
              value={formData.experience2}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            />
          </label>
          <label className="block mt-4 mb-2 font-medium">
            Experience 2 Highlights:
            <textarea
              name="experience2_highlights"
              placeholder='Work experience highlights'
              value={formData.experience2_highlights}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            />
          </label>
        </div>

        <div>
          <label className="block mb-2 font-medium">
            Experience 3 (Company Name):
            <textarea
              name="experience3"
              placeholder='Enter company name'
              value={formData.experience3}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            />
          </label>
          <label className="block mt-4 mb-2 font-medium">
            Experience 3 Highlights:
            <textarea
              name="experience3_highlights"
              placeholder='Work experience highlights'
              value={formData.experience3_highlights}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            />
          </label>
        </div>

       

     

      


        {/* Submit Button */}
        <button type="submit" className="bg-blue-500 text-white py-2 px-4 rounded-md">
          Generate Resume
        </button>
      </form>
    </div>
  );
}
