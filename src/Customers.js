```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await axios.get('/api/customers');
        setCustomers(response.data);
      } catch (error) {
        console.error("Error fetching customers:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchCustomers();
  }, []);

  const deleteCustomer = async (id) => {
    try {
      await axios.delete(`/api/customers/${id}`);
      setCustomers(customers.filter(customer => customer.id !== id));
    } catch (error) {
      console.error("Error deleting customer:", error);
    }
  };

  return (
    <div>
      <h1>Customer List</h1>
      {loading ? <p>Loading...</p> : (
        <ul>
          {customers.map(customer => (
            <li key={customer.id}>
              {customer.name} - {customer.email}
              <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CustomerList;
```