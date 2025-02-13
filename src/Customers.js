```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchCustomers = async () => {
            setLoading(true);
            const response = await axios.get('/api/customers');
            setCustomers(response.data);
            setLoading(false);
        };
        fetchCustomers();
    }, []);

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleSearch = (event) => {
        setSearchTerm(event.target.value);
    };

    return (
        <div>
            <input 
                type="text" 
                placeholder="Search Customers" 
                value={searchTerm} 
                onChange={handleSearch} 
            />
            {loading ? (
                <p>Loading...</p>
            ) : (
                <ul>
                    {filteredCustomers.map(customer => (
                        <li key={customer.id}>
                            {customer.name} - {customer.email}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default CustomerManagement;
```