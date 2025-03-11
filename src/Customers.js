```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = ({ customers }) => {
    const [sortedCustomers, setSortedCustomers] = useState([]);

    useEffect(() => {
        setSortedCustomers([...customers].sort((a, b) => a.name.localeCompare(b.name)));
    }, [customers]);

    const handleDelete = (id) => {
        // logic to delete customer (usually involves calling API)
    };

    return (
        <div>
            <h2>Customer List</h2>
            <ul>
                {sortedCustomers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} - {customer.email}
                        <button onClick={() => handleDelete(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```