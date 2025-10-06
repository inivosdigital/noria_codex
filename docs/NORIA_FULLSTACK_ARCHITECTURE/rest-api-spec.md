# REST API Spec

```yaml
openapi: 3.0.0
info:
  title: Noria AI Social Coaching API
  version: 1.0.0
  description: Backend API for Noria's evidence-based social coaching platform
servers:
  - url: https://noria-app.vercel.app/api
    description: Production API
  - url: http://localhost:3000/api
    description: Local development
paths:
  /auth/signup:
    post:
      summary: Create new user account
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
                goals:
                  type: array
                  items:
                    $ref: '#/components/schemas/SocialGoal'
      responses:
        201:
          description: Account created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        400:
          $ref: '#/components/responses/ValidationError'

  /chat/send:
    post:
      summary: Send message to AI coach
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  maxLength: 2000
      responses:
        200:
          description: Coach response generated
          content:
            application/json:
              schema:
                type: object
                properties:
                  response:
                    type: string
                  message_id:
                    type: string
                  crisis_detected:
                    type: boolean
                  resources:
                    type: array
                    items:
                      $ref: '#/components/schemas/CrisisResource'

  /chat/history:
    get:
      summary: Get conversation history
      security:
        - bearerAuth: []
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 50
        - name: before
          in: query
          schema:
            type: string
      responses:
        200:
          description: Conversation history
          content:
            application/json:
              schema:
                type: object
                properties:
                  messages:
                    type: array
                    items:
                      $ref: '#/components/schemas/Conversation'

  /analysis/trigger:
    post:
      summary: Manually trigger conversation analysis
      security:
        - bearerAuth: []
      responses:
        202:
          description: Analysis queued for processing

  /user/profile:
    get:
      summary: Get user profile
      security:
        - bearerAuth: []
      responses:
        200:
          description: User profile data
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
    patch:
      summary: Update user profile
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                goals:
                  type: array
                  items:
                    $ref: '#/components/schemas/SocialGoal'
                preferences:
                  $ref: '#/components/schemas/UserPreferences'

  /wellness/resources:
    get:
      summary: Get wellness resources
      responses:
        200:
          description: Available wellness resources
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/WellnessResource'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
        goals:
          type: array
          items:
            $ref: '#/components/schemas/SocialGoal'
        stage:
          $ref: '#/components/schemas/CoachingStage'
        profile:
          $ref: '#/components/schemas/UserProfile'
        created_at:
          type: string
          format: date-time
        last_active:
          type: string
          format: date-time
    
    SocialGoal:
      type: string
      enum:
        - build_confidence
        - make_friends
        - improve_conversations
        - overcome_anxiety
        - join_activities
        - dating_skills
        - roommate_relations
    
    CoachingStage:
      type: integer
      enum: [1, 2, 3]
    
    Conversation:
      type: object
      properties:
        id:
          type: string
        user_id:
          type: string
        message_text:
          type: string
        sender_type:
          type: string
          enum: [user, assistant]
        timestamp:
          type: string
          format: date-time
        message_metadata:
          type: object

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  responses:
    ValidationError:
      description: Validation error
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: object
                properties:
                  code:
                    type: string
                  message:
                    type: string
                  details:
                    type: object
```
