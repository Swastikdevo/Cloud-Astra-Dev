```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await fetch('/api/customers');
        const data = await response.json();
        setCustomers(data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchCustomers();
  }, []);

  const renderCustomerRow = (customer) => (
    <tr key={customer.id}>
      <td>{customer.name}</td>
      <td>{customer.email}</td>
      <td>{customer.phone}</td>
      <td>
        <button onClick={() => handleEdit(customer.id)}>Edit</button>
        <button onClick={() => handleDelete(customer.id)}>Delete</button>
      </td>
    </tr>
  );

  const handleEdit = (id) => {
    // Edit logic here
  };

  const handleDelete = (id) => {
    // Delete logic here
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error fetching customers: {error.message}</p>;
  
  return (
    <div>
      <h1>Customer Management</h1>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {customers.map(renderCustomerRow)}
        </tbody>
      </table>
    </div>
  );
};

export default CustomerManagement;
```