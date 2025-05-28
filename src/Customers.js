```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => {
        setCustomers(data);
        setLoading(false);
      })
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {customers.map(customer => (
            <li key={customer.id}>
              {customer.name} - {customer.email}
              <button onClick={() => alert(`Editing ${customer.name}`)}>Edit</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CustomerList;
```