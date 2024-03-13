import React, { useState, useEffect } from 'react';
import './Notification.css'; // Import CSS file for notification styling

const Notification = () => {
  const [showNotification, setShowNotification] = useState(false);

  useEffect(() => {
    // Show notification
    setShowNotification(true);

    // Hide notification after 3 seconds
    const timer = setTimeout(() => {
      setShowNotification(false);
    }, 3000);

    // Cleanup timer on component unmount
    return () => clearTimeout(timer);
  }, []); // Empty dependency array ensures useEffect runs only once on component mount

  return (
    <div className={`notification ${showNotification ? 'show' : ''}`}>
      Notification Message
    </div>
  );
};

export default Notification;
