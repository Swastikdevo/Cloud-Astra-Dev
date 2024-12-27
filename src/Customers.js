```javascript
import React, { useState, useEffect } from 'react';

const CustomerProfile = ({ customerId }) => {
  const [customer, setCustomer] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomer = async () => {
      const response = await fetch(`/api/customers/${customerId}`);
      const data = await response.json();
      setCustomer(data);
      setLoading(false);
    };
    fetchCustomer();
  }, [customerId]);

  const handleUpdate = async (updatedInfo) => {
    await fetch(`/api/customers/${customerId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedInfo),
    });
    setCustomer((prev) => ({ ...prev, ...updatedInfo }));
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>{customer.name}</h2>
      <p>Email: {customer.email}</p>
      <button onClick={() => handleUpdate({ name: 'New Name' })}>Update Name</button>
    </div>
  );
};

export default CustomerProfile;
```