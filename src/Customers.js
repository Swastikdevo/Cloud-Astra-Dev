```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => {
        setCustomers(data);
        setIsLoading(false);
      })
      .catch(error => {
        console.error('Error fetching customers:', error);
        setIsLoading(false);
      });
  }, []);

  const handleDelete = (id) => {
    fetch(`/api/customers/${id}`, {
      method: 'DELETE'
    })
      .then(() => {
        setCustomers(customers.filter(customer => customer.id !== id));
      })
      .catch(error => console.error('Error deleting customer:', error));
  };

  return (
    <div>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {customers.map(customer => (
            <li key={customer.id}>
              {customer.name}
              <button onClick={() => handleDelete(customer.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CustomerList;
```