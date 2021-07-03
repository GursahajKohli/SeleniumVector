from scrapy.item import Item, Field


class JobDetails(Item):
    """
    Job Details XML Fields, as per: https://support.jobboard.io/docs/setting-up-3rd-party-xml-job-imports#available-fields
    """
    title           = Field(serializer=str)     # The title of the job (required)
    company         = Field(serializer=str)     # The hiring company (required)
    location        = Field(serializer=str)     # The complete job location (required)
    description     = Field(serializer=str)     # The job description (required)
    url             = Field(serializer=str)     # If the application form is hosted elsewhere, add the link here. (required)
    email           = Field(serializer=str)     # Where should applications be sent to? (required)
    city            = Field(serializer=str)     # The City where the job is located (required)
    state           = Field(serializer=str)     # The State where the job is located. For non-US jobs, you may map the country field here (required)
    company_url     = Field(serializer=str)     # A link to the company website
    remote          = Field(serializer=bool)    # Is the job remote? True or False
    zip             = Field(serializer=str)     # The Zip or Postal code where the job is located
    country         = Field(serializer=str)     # The Country where the job is located
    category        = Field(serializer=str)     # The category for the job.
    reference       = Field(serializer=str)     # Set the unique reference ID for the job
    logo            = Field(serializer=str)     # Link to the employer logo
    salary          = Field(serializer=int)     # What is the salary for this job?
    posting_date    = Field(serializer=str)     # Set a posting date for the job. If left blank, we'll use the time the job is created in our system. Required format is: MM/DD/YYYY
    jobtype         = Field(serializer=str)     # Is this position Full Time? Part Time? Be sure the value used matches a job type that's been set up under 'Job Types' in your admin panel. If no type is provided, the default job type will be used.
    expiration_date = Field(serializer=str)     # Set the expiration date. If no date is provided, we will use the default posting length for you site. Required format is: MM/DD/YYYY
